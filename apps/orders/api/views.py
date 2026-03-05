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


