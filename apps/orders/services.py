from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import base64
import uuid
from apps.catalog.models import Flower, BouquetSize
from apps.bouquet.models import Bouquet, BouquetItem
from apps.discounts.models import Coupon
from apps.orders.models import Order
from django.conf import settings
from decimal import Decimal

def create_order(request, *, user=None, guest_data=None, size_code, flowers_data, wrap_data=None, coupon_code=None):
    """
    Orchestrates the order creation process with server-side price validation.
    """
    
    # 1. Validate Bouquet Size
    try:
        size = BouquetSize.objects.get(code=size_code)
    except BouquetSize.DoesNotExist:
        raise ValidationError(f"El tamaño de ramo '{size_code}' no existe.")

    # 2. Validate Tier Limits and fetch DB prices
    tier_counts = {'l': 0, 'm': 0, 's': 0}
    flower_ids = [f['flower_id'] for f in flowers_data]
    flowers_db = {f.id: f for f in Flower.objects.filter(id__in=flower_ids, is_active=True)}
    
    for f_data in flowers_data:
        flower = flowers_db.get(f_data['flower_id'])
        if not flower:
            raise ValidationError(f"Flor con ID {f_data['flower_id']} no existe o no está activa.")
        tier_counts[flower.tier] += 1

    if tier_counts['l'] > size.max_large:
        raise ValidationError(f"Exceso de flores grandes: máximo {size.max_large}, recibidas {tier_counts['l']}.")
    if tier_counts['m'] > size.max_medium:
        raise ValidationError(f"Exceso de flores medianas: máximo {size.max_medium}, recibidas {tier_counts['m']}.")
    if tier_counts['s'] > size.max_small:
        raise ValidationError(f"Exceso de flores pequeñas: máximo {size.max_small}, recibidas {tier_counts['s']}.")

    with transaction.atomic():
        # 3. Create Bouquet
        bouquet = Bouquet.objects.create(size=size, user=user)
        
        total_flowers_price = Decimal('0.00')
        for f_data in flowers_data:
            flower = flowers_db[f_data['flower_id']]
            
            # Stock management validation only (decrement moved to confirmation)
            if flower.stock <= 0:
                raise ValidationError(f"Lo sentimos, no hay stock suficiente de {flower.name}.")

            BouquetItem.objects.create(
                bouquet=bouquet,
                flower=flower,
                x=f_data['x'],
                y=f_data['y'],
                scale=f_data.get('scale', 1.0),
                rotation=f_data.get('rotation', 0.0),
                price_snapshot=flower.price
            )
            total_flowers_price += flower.price
        
        bouquet.total_price = size.base_price + total_flowers_price
        bouquet.save()

        # 4. Handle Discount/Coupon Logic
        discount_amount = Decimal('0.00')
        coupon = None
        
        # Best applicable discount logic
        discount_amount = _calculate_best_discount(bouquet, coupon_code)

        # 5. Create Order
        # UUID is handled by default in the model now
        order = Order.objects.create(
            user=user,
            guest_name=guest_data.get('name') if guest_data else None,
            guest_email=guest_data.get('email') if guest_data else None,
            guest_phone=guest_data.get('phone') if guest_data else None,
            bouquet=bouquet,
            total_amount=bouquet.total_price,
            discount_amount=discount_amount,
            final_amount=bouquet.total_price - discount_amount
        )

        # 5.5 Generate Bouquet Image server-side using Pillow
        try:
            img_file = _generate_bouquet_image_pillow(order.bouquet, str(order.tracking_token), wrap_data)
            if img_file:
                order.bouquet_image.save(img_file[0], img_file[1], save=True)
        except Exception as e:
            print(f"Error generating bouquet image: {e}")

    # 6. Generate WhatsApp Message
    whatsapp_message_text = _generate_whatsapp_message(request, order)

    return order, whatsapp_message_text 

def _calculate_best_discount(bouquet, coupon_code):
    from django.utils import timezone
    from apps.discounts.models import Discount, Coupon
    now = timezone.now()
    best_discount = Decimal('0.00')

    # 1. Check Coupon if provided (legacy/code-based)
    if coupon_code:
        try:
            c = Coupon.objects.get(code=coupon_code, is_active=True, valid_from__lte=now, valid_to__gte=now)
            best_discount = (bouquet.total_price * c.discount_percentage) / 100
        except Coupon.DoesNotExist:
            pass

    # 2. Check Automatic Discounts
    active_discounts = Discount.objects.filter(is_active=True, valid_from__lte=now, valid_to__gte=now)
    
    for d in active_discounts:
        current_d = Decimal('0.00')
        if d.type == 'global':
            if d.percentage > 0:
                current_d = (bouquet.total_price * d.percentage) / 100
            else:
                current_d = d.fixed_amount
        
        elif d.type == 'category' and d.tier_target:
            # Apply only to items with the matching tier
            matching_total = Decimal('0.00')
            for item in bouquet.items.all():
                if item.flower.tier == d.tier_target:
                    matching_total += item.price_snapshot
            
            if matching_total > 0:
                if d.percentage > 0:
                    current_d = (matching_total * d.percentage) / 100
                else:
                    current_d = d.fixed_amount
        
        elif d.type == 'product' and d.flower_target:
            # Apply only to the specific flower
            found = False
            matching_total = Decimal('0.00')
            for item in bouquet.items.all():
                if item.flower == d.flower_target:
                    matching_total += item.price_snapshot
                    found = True
            
            if found:
                if d.percentage > 0:
                    current_d = (matching_total * d.percentage) / 100
                else:
                    current_d = d.fixed_amount
        
        if current_d > best_discount:
            best_discount = current_d

    return best_discount.quantize(Decimal('0.01'))

def _generate_whatsapp_message(request, order):
    from collections import Counter
    client_name = order.user.get_full_name() if order.user else (order.guest_name or "Invitado")
    size_name = order.bouquet.size.name if order.bouquet and order.bouquet.size else "Estándar"

    flower_counts = Counter(item.flower.name for item in order.bouquet.items.all())
    flower_lines = "\n".join(
        f"  - {name}: {count}" for name, count in flower_counts.items()
    )

    price_lines = f"  Subtotal: ${order.total_amount:.2f}"
    if order.discount_amount > 0:
        price_lines += f"\n  Descuento: -${order.discount_amount:.2f}"
    price_lines += f"\n  Total Final: ${order.final_amount:.2f}"

    msg = (
        f"Hola, soy {client_name} y me gustaria confirmar mi pedido.\n\n"
        f"*Ramo Personalizado - Tamano {size_name}*\n"
        f"{flower_lines}\n\n"
        f"{price_lines}\n\n"
        f"Mi numero de pedido es el *#{order.id}*. Me podrias confirmar el pedido, por favor?"
    )
    return msg


def _generate_bouquet_image_pillow(bouquet, tracking_token, wrap_data=None):
    """
    Generate a bouquet image server-side using Pillow.
    Composites wrap (back), flower PNG images, and wrap (front) onto a beige canvas.
    """
    try:
        from PIL import Image, ImageDraw, ImageColor, ImageChops, ImageEnhance
        import io, os
        from django.conf import settings

        # Match frontend 400x650 aspect ratio (1.625)
        # Using 600x975 (600 * 1.625 = 975)
        W, H = 600, 975
        # Light beige background
        base = Image.new('RGBA', (W, H), (253, 249, 244, 255))

        # Helper to load and process wrap color
        def get_wrap_layer(color_hex):
            if not color_hex: color_hex = "#e8dfcc"
            texture_path = os.path.join(settings.MEDIA_ROOT, "envoltura.png")
            if not os.path.exists(texture_path):
                return None
            
            texture = Image.open(texture_path).convert('RGBA')
            rgb = ImageColor.getrgb(color_hex)
            color_layer = Image.new('RGBA', texture.size, rgb + (255,))
            mult_rgb = ImageChops.multiply(texture.convert('RGB'), color_layer.convert('RGB'))
            result = mult_rgb.convert('RGBA')
            result.putalpha(texture.getchannel('A'))
            return result

        wrap_color = wrap_data.get('color') if wrap_data else "#e8dfcc"
        wrap_scale = float(wrap_data.get('scale', 1.0)) if wrap_data else 1.0
        wrap_x_off = float(wrap_data.get('x', 0)) if wrap_data else 0
        wrap_y_off = float(wrap_data.get('y', 0)) if wrap_data else 0

        # Draw Wrap Back
        wrap_img = get_wrap_layer(wrap_color)
        pos_x, pos_y = 0, 0
        sw, sh = 0, 0
        if wrap_img:
            sw = int(460 * wrap_scale * 1.5)
            sh = int(wrap_img.height * (sw / wrap_img.width))
            wrap_img_scaled = wrap_img.resize((sw, sh), Image.LANCZOS)
            back_img = ImageEnhance.Brightness(wrap_img_scaled).enhance(0.85)
            pos_x = (W // 2) - (sw // 2) + int(wrap_x_off * 1.5)
            pos_y = H - sh + int(50 * 1.5) + int(wrap_y_off * 1.5)
            base.paste(back_img, (pos_x, pos_y), back_img)

        # Draw Flowers
        items = list(bouquet.items.all().select_related('flower'))
        for item in items:
            flower = item.flower
            if not flower.image or not flower.image.name: continue
            img_path = flower.image.path
            if not os.path.exists(img_path): continue
            
            f_img = Image.open(img_path).convert('RGBA')
            
            # Intelligent Stem Hiding (Gradient Mask)
            # Replicates CSS: mask-image: linear-gradient(to bottom, black 35%, transparent 68%)
            w, h = f_img.size
            # Vectorized gradient using numpy (much faster than pixel-by-pixel loop)
            try:
                import numpy as np
                ys = np.arange(h, dtype=np.float32)
                alphas = np.where(
                    ys < 0.35 * h, 255,
                    np.where(
                        ys > 0.68 * h, 0,
                        (255 * (1 - (ys - 0.35 * h) / (0.68 * h - 0.35 * h))).astype(np.float32)
                    )
                ).clip(0, 255).astype(np.uint8)
                col_mask = Image.fromarray(alphas[:, np.newaxis], mode='L')
            except ImportError:
                # Fallback: still use pixel loop if numpy is unavailable
                col_mask = Image.new('L', (1, h), 255)
                for y in range(h):
                    if y < 0.35 * h:
                        alpha = 255
                    elif y > 0.68 * h:
                        alpha = 0
                    else:
                        ratio = (y - 0.35 * h) / (0.68 * h - 0.35 * h)
                        alpha = int(255 * (1 - ratio))
                    col_mask.putpixel((0, y), alpha)

            mask = col_mask.resize((w, h), Image.NEAREST)
            f_img.putalpha(ImageChops.multiply(f_img.getchannel('A'), mask))

            base_size = 200
            scaled_size = int(base_size * float(item.scale) * (W / 400))
            scaled_size = max(30, min(scaled_size, W))
            f_img = f_img.resize((scaled_size, scaled_size), Image.LANCZOS)
            f_img = f_img.rotate(-float(item.rotation), expand=True, resample=Image.BICUBIC)
            
            cx, cy = int((float(item.x)/100)*W), int((float(item.y)/100)*H)
            base.paste(f_img, (cx - f_img.width//2, cy - f_img.height//2), f_img)

        # Draw Wrap Front (Clipped)
        if wrap_img:
            front_img = wrap_img_scaled 
            mask = Image.new('L', front_img.size, 0)
            draw = ImageDraw.Draw(mask)
            w_pts, h_pts = front_img.size
            poly = [
                (0, h_pts * 0.42),
                (w_pts * 0.48, h_pts * 0.68),
                (w_pts * 0.52, h_pts * 0.68),
                (w_pts, h_pts * 0.42),
                (w_pts, h_pts),
                (0, h_pts)
            ]
            draw.polygon(poly, fill=255)
            final_mask = ImageChops.multiply(front_img.getchannel('A'), mask)
            base.paste(front_img, (pos_x, pos_y), final_mask)

        # Save to bytes
        output = io.BytesIO()
        base.convert('RGB').save(output, format='JPEG', quality=90)
        output.seek(0)
        filename = f"bouquet_{tracking_token}.jpg"
        return (filename, ContentFile(output.read(), name=filename))

    except Exception as e:
        print(f"Pillow compositing error: {e}")
        import traceback
        traceback.print_exc()
        return None
