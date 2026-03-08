"""
Quick Order API — for pre-designed products (Promotion, Service, PreDesignedBouquet)
that don't go through the custom bouquet designer.

POST /orders/quick-order/
{
    "product_type": "promotion" | "service" | "predesigned",
    "product_id": <int>,
    "guest_data": {"name": "...", "phone": "..."}  // only for guests
}
"""
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal
import uuid

from apps.orders.models import Order
from apps.bouquet.models import Bouquet, BouquetItem
from apps.catalog.models import Promotion, Service, PreDesignedBouquet, BouquetSize


@method_decorator(csrf_exempt, name='dispatch')
class QuickOrderCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        product_type = data.get('product_type')
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        guest_data = data.get('guest_data')
        user = request.user if request.user.is_authenticated else None

        if not user and not guest_data:
            return JsonResponse({'error': 'Se requieren datos de invitado o estar logueado.'}, status=400)

        if not product_type or not product_id:
            return JsonResponse({'error': 'Faltan campos requeridos (product_type, product_id).'}, status=400)

        if quantity < 1:
            return JsonResponse({'error': 'La cantidad debe ser al menos 1.'}, status=400)

        # Resolve product
        try:
            if product_type == 'promotion':
                product = Promotion.objects.get(id=product_id, is_active=True)
                name = product.name
                price = product.price
                image_field = product.image
                description = ""
                note = f"Promoción: {product.name}"
            elif product_type == 'predesigned':
                product = PreDesignedBouquet.objects.get(id=product_id, is_active=True)
                if product.stock < quantity:
                    return JsonResponse({'error': f'Lo sentimos, soló tenemos {product.stock} unidades de "{product.name}" disponibles.'}, status=400)
                product.stock -= quantity
                product.save()
                name = product.name
                price = product.price
                image_field = product.image
                description = product.description
                note = f"Ramo Pre-diseñado: {product.name}"
            elif product_type == 'service':
                product = Service.objects.get(id=product_id, is_active=True)
                # Some services might not be "countable" or have stock, but let's assume they might.
                # If service lacks a stock field or works differently here, this handles stock > 0 loosely.
                if hasattr(product, 'stock') and product.stock < quantity:
                    return JsonResponse({'error': f'Lo sentimos, no hay disponibilidad suficiente para el servicio "{product.title}".'}, status=400)
                name = product.title
                price = product.price
                image_field = product.image
                description = product.description
                note = f"Servicio: {product.title}"
            else:
                return JsonResponse({'error': 'Tipo de producto no válido.'}, status=400)
        except (Promotion.DoesNotExist, PreDesignedBouquet.DoesNotExist, Service.DoesNotExist):
            return JsonResponse({'error': 'Producto no encontrado o no disponible.'}, status=404)

        # Create a minimal placeholder bouquet (required by Order model)
        size_qs = BouquetSize.objects.first()
        if not size_qs:
            return JsonResponse({'error': 'No hay tamaños de ramo configurados en el sistema.'}, status=500)

        total_order_price = price * quantity

        bouquet = Bouquet.objects.create(size=size_qs, user=user, total_price=total_order_price)

        order = Order.objects.create(
            user=user,
            guest_name=guest_data.get('name') if guest_data else None,
            guest_email=guest_data.get('email', f"guest_{uuid.uuid4().hex[:8]}@sisart.com") if guest_data else None,
            guest_phone=guest_data.get('phone', '') if guest_data else None,
            bouquet=bouquet,
            item_type=product_type,
            item_name=name,
            item_description=description,
            item_image=image_field,
            total_amount=total_order_price,
            discount_amount=Decimal('0.00'),
            final_amount=total_order_price,
        )

        # WhatsApp message (friendly, from client to seller)
        client_name = user.get_full_name() if user else (guest_data.get('name', 'Invitado') if guest_data else 'Invitado')
        
        whatsapp_msg = (
            f"¡Hola! 👋 Me gustaría hacer un pedido.\n\n"
            f"Soy {client_name}.\n"
            f"Me interesa adquirir:\n"
            f"🌸 {quantity}x {note}\n"
            f"💵 Total: ${total_order_price:.2f}\n\n"
            f"Mi número de pedido pre-registrado es el #{order.id}. ¿Me podrían ayudar confirmando mi compra, por favor? ✨"
        )

        return JsonResponse({
            'id': order.id,
            'status': 'success',
            'whatsapp_message': whatsapp_msg,
            'tracking_token': str(order.tracking_token),
            'total': float(total_order_price),
        }, status=201)
