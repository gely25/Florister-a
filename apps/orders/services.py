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
    Orchestrates the order creation process.
    flowers_data: list of dicts {'flower_id': int, 'x': float, 'y': float, 'scale': float, 'rotation': float}
    """
    
    # 1. Validate Bouquet Size
    try:
        size = BouquetSize.objects.get(code=size_code)
    except BouquetSize.DoesNotExist:
        raise ValidationError(f"El tamaño de ramo '{size_code}' no existe.")

    # 2. Validate Tier Limits
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
        bouquet = Bouquet.objects.create(size=size)
        
        total_flowers_price = Decimal('0.00')
        for f_data in flowers_data:
            flower = flowers_db[f_data['flower_id']]
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

        # 4. Handle Discount
        discount_amount = Decimal('0.00')
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                # Validation of dates could be added here
                discount_amount = (bouquet.total_price * coupon.discount_percentage) / 100
            except Coupon.DoesNotExist:
                raise ValidationError(f"Cupón '{coupon_code}' no es válido.")

        # 5. Create Order
        order = Order.objects.create(
            user=user,
            guest_name=guest_data.get('name') if guest_data else None,
            guest_email=guest_data.get('email') if guest_data else None,
            guest_phone=guest_data.get('phone') if guest_data else None,
            bouquet=bouquet,
            coupon=coupon,
            total_amount=bouquet.total_price,
            discount_amount=discount_amount,
            final_amount=bouquet.total_price - discount_amount
        )

        # 5.5 Generate Bouquet Image server-side using Pillow
        try:
            img_file = _generate_bouquet_image_pillow(order.bouquet, order.tracking_token, wrap_data)
            if img_file:
                order.bouquet_image.save(img_file[0], img_file[1], save=True)
        except Exception as e:
            print(f"Error generating bouquet image: {e}")


    # 6. Generate WhatsApp Message
    whatsapp_message = _generate_whatsapp_message(request, order)

    return order, whatsapp_message

def _generate_whatsapp_message(request, order):
    msg = f"*Nuevo Pedido #{order.id}*\n\n"
    msg += f"Cliente: {order.user.get_full_name() if order.user else order.guest_name}\n"
    msg += f"Tamaño: {order.bouquet.size.name}\n"
    msg += f"Flores:\n"
    from collections import Counter
    
    flower_counts = Counter(item.flower.name for item in order.bouquet.items.all())
    for name, count in flower_counts.items():
        msg += f"- {name}: {count}\n"
    
    msg += f"\n*Resumen*\n"
    msg += f"Subtotal: ${order.total_amount}\n"
    if order.discount_amount > 0:
        msg += f"Descuento: -${order.discount_amount} ({order.coupon.code})\n"
    msg += f"Total Final: ${order.final_amount}\n\n"
    
    # Public Tracking Link
    tracking_url = request.build_absolute_uri(f"/orders/track/{order.tracking_token}/")
    msg += f"Sigue tu pedido aquí: {tracking_url}\n\n"
    
    if order.bouquet_image:
        image_url = request.build_absolute_uri(order.bouquet_image.url)
        msg += f"{image_url}\n"
        
    msg += "¡Gracias por preferir Atelier Floral!"
    
    return msg


def _generate_bouquet_image_pillow(bouquet, tracking_token, wrap_data=None):
    """
    Generate a bouquet image server-side using Pillow.
    Composites wrap (back), flower PNG images, and wrap (front) onto a beige canvas.
    """
    try:
        from PIL import Image, ImageDraw, ImageColor, ImageChops, ImageEnhance
        import io, os

        W, H = 600, 900
        # Beige background matching the designer UI
        base = Image.new('RGBA', (W, H), (253, 249, 244, 255))

        # Helper to load and process wrap color
        def get_wrap_layer(color_hex):
            if not color_hex: color_hex = "#e8dfcc"
            texture_path = os.path.join(settings.MEDIA_ROOT, "envoltura.png")
            if not os.path.exists(texture_path):
                return None
            
            # Load texture
            texture = Image.open(texture_path).convert('RGBA')
            
            # 1. Create a solid color layer of the same size
            rgb = ImageColor.getrgb(color_hex)
            color_layer = Image.new('RGBA', texture.size, rgb + (255,))
            
            # 2. Replicate mix-blend-mode: multiply
            # We want: (Texture RGB * Color RGB) inside the Texture Alpha
            # First, multiply the RGB channels
            mult_rgb = ImageChops.multiply(texture.convert('RGB'), color_layer.convert('RGB'))
            
            # 3. Handle the Ribbon (Lazo)
            # If the ribbon is part of the texture and should NOT be colored,
            # we need to detect it. But since we don't know the coordinates,
            # usually these textures have the ribbon in the alpha channel but with 
            # original colors in the RGB. 
            # Actually, a better approach for "multiply" in Pillow while keeping alpha:
            result = mult_rgb.convert('RGBA')
            result.putalpha(texture.getchannel('A'))
            
            return result

        wrap_color = wrap_data.get('color') if wrap_data else "#e8dfcc"
        wrap_scale = float(wrap_data.get('scale', 1.0)) if wrap_data else 1.0
        wrap_x_off = float(wrap_data.get('x', 0)) if wrap_data else 0
        wrap_y_off = float(wrap_data.get('y', 0)) if wrap_data else 0

        # Draw Wrap Back
        wrap_img = get_wrap_layer(wrap_color)
        if wrap_img:
            # Scale wrap image (Base width 460px in frontend, stage 400px)
            # Our canvas is 600px, so we scale proportionally 600/400 = 1.5
            sw = int(460 * wrap_scale * 1.5)
            sh = int(wrap_img.height * (sw / wrap_img.width))
            wrap_img_scaled = wrap_img.resize((sw, sh), Image.LANCZOS)
            
            # Darken back part (CSS: filter: brightness(0.85))
            back_img = ImageEnhance.Brightness(wrap_img_scaled).enhance(0.85)
            
            # Position (CSS: bottom -50px, left 50%, translateX(-50%))
            # In 600x900 canvas:
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
            base_size = 200
            scaled_size = int(base_size * float(item.scale) * (W / 400))
            scaled_size = max(30, min(scaled_size, W))
            f_img = f_img.resize((scaled_size, scaled_size), Image.LANCZOS)
            f_img = f_img.rotate(-float(item.rotation), expand=True, resample=Image.BICUBIC)
            
            cx, cy = int((float(item.x)/100)*W), int((float(item.y)/100)*H)
            base.paste(f_img, (cx - f_img.width//2, cy - f_img.height//2), f_img)

        # Draw Wrap Front (Clipped)
        if wrap_img:
            # Darken front just slightly if needed, or keep original
            front_img = wrap_img_scaled 
            
            # Apply Clip Path: polygon(0 42%, 48% 68%, 52% 68%, 100% 42%, 100% 100%, 0 100%)
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
            
            # Combine front image alpha with the clip mask
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
