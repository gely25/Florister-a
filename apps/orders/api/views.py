import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from apps.orders.services import create_order
from django.core.exceptions import ValidationError

@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        user = request.user if request.user.is_authenticated else None
        guest_data = data.get('guest_data')
        size_code = data.get('size_id') # Standardizing key from frontend
        flowers_data = data.get('flowers', [])
        wrap_data = data.get('wrap_data')
        coupon_code = data.get('coupon_code')

        if not user and not guest_data:
            return JsonResponse({'error': 'Se requieren datos de invitado o estar logueado.'}, status=400)

        try:
            order, whatsapp_msg = create_order(
                request,
                user=user,
                guest_data=guest_data,
                size_code=size_code,
                flowers_data=flowers_data,
                wrap_data=wrap_data,
                coupon_code=coupon_code
            )
            return JsonResponse({
                'id': order.id,
                'status': 'success',
                'whatsapp_message': whatsapp_msg,
                'tracking_token': order.tracking_token,
                'total': float(order.final_amount)
            }, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e.message) if hasattr(e, 'message') else str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)

from django.shortcuts import render

class TrackOrderStubView(View):
    def get(self, request, token, *args, **kwargs):
        from apps.orders.models import Order
        from django.db.models import Count
        try:
            order = Order.objects.get(tracking_token=token)
            
            is_staff = request.user.is_authenticated and request.user.is_staff
            recipe = None
            
            if is_staff:
                # Aggregate flower counts for the florist
                from apps.bouquet.models import BouquetItem
                recipe = BouquetItem.objects.filter(bouquet=order.bouquet).values(
                    'flower__name', 'flower__image', 'flower__tier'
                ).annotate(total=Count('flower'))
            
            context = {
                'order': order,
                'is_staff': is_staff,
                'recipe': recipe,
                'status_choices': Order.STATUS_CHOICES
            }
            return render(request, 'orders/track.html', context)
        except Order.DoesNotExist:
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound("<h1>Pedido no encontrado</h1>")

    def post(self, request, token, *args, **kwargs):
        """Staff can update order status from the tracking page."""
        from apps.orders.models import Order
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'No autorizado'}, status=403)
            
        try:
            order = Order.objects.get(tracking_token=token)
            new_status = request.POST.get('status')
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                return JsonResponse({'status': 'success', 'new_status': order.get_status_display()})
            return JsonResponse({'error': 'Estado no válido'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Pedido no encontrado'}, status=404)
