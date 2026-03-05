from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.catalog.views import SellerRequiredMixin
from django.contrib import messages
from .models import Order

class OrderListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

class OrderManagementDetailView(LoginRequiredMixin, SellerRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_management_detail.html'
    context_object_name = 'order'

class OrderStatusUpdateView(LoginRequiredMixin, SellerRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({
                'status': 'success', 
                'message': f"Estado actualizado a {order.get_status_display()}."
            })
        return JsonResponse({'status': 'error', 'error': 'Estado no válido'}, status=400)

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/track.html'
    context_object_name = 'order'
    slug_field = 'tracking_token'
    slug_url_kwarg = 'token'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        is_staff = self.request.user.is_authenticated and self.request.user.is_staff
        
        if is_staff:
            from apps.bouquet.models import BouquetItem
            from django.db.models import Count
            context['recipe'] = BouquetItem.objects.filter(bouquet=order.bouquet).values(
                'flower__name', 'flower__image', 'flower__tier'
            ).annotate(total=Count('flower'))
            context['status_choices'] = Order.STATUS_CHOICES
            
        context['is_staff'] = is_staff
        return context

class TrackOrderSearchView(View):
    """
    Search view for tracking orders by token.
    """
    def get(self, request):
        token = request.GET.get('token')
        if token:
            return redirect('orders:track', token=token.strip())
        return render(request, 'orders/track.html')

    def post(self, request):
        token = request.POST.get('token')
        if token:
            return redirect('orders:track', token=token.strip())
        return render(request, 'orders/track.html', {'error': 'Por favor ingresa un código válido.'})
