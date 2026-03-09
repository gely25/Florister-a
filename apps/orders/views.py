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
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            if search_query.isdigit():
                queryset = queryset.filter(id=search_query)
            else:
                queryset = queryset.filter(tracking_token__icontains=search_query)
                
        # Status filtering
        status_filter = self.request.GET.get('status', '').strip()
        if status_filter and status_filter in dict(Order.STATUS_CHOICES):
            queryset = queryset.filter(status=status_filter)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Order.STATUS_CHOICES
        return context

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
            messages.success(request, f"Estado del pedido #{order.id} actualizado a {order.get_status_display()}.")
        else:
            messages.error(request, 'Estado no válido.')
            
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('orders:management_list')

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            if search_query.isdigit():
                queryset = queryset.filter(id=search_query)
            else:
                queryset = queryset.filter(tracking_token__icontains=search_query)
                
        # Status filtering
        status_filter = self.request.GET.get('status', '').strip()
        if status_filter and status_filter in dict(Order.STATUS_CHOICES):
            queryset = queryset.filter(status=status_filter)
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Order.STATUS_CHOICES
        return context

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
        user = self.request.user
        
        # Security: If user is authenticated and order belongs to a user, 
        # ensure it's their own order or they are staff.
        is_owner = not order.user or (user.is_authenticated and order.user == user)
        is_staff = user.is_authenticated and user.is_staff
        
        if not is_owner and not is_staff:
            # Silently redirect to home or show error if they try to peek at others' orders
            context['unauthorized'] = True
            
        if is_staff:
            from apps.bouquet.models import BouquetItem
            from django.db.models import Count
            context['recipe'] = BouquetItem.objects.filter(bouquet=order.bouquet).values(
                'flower__name', 'flower__image', 'flower__tier'
            ).annotate(total=Count('flower'))
            context['status_choices'] = Order.STATUS_CHOICES
            
        context['is_staff'] = is_staff
        context['is_owner'] = is_owner
        return context

class TrackOrderSearchView(View):
    """
    Search view for tracking orders by token.
    """
    def get(self, request):
        token = request.GET.get('token')
        if token:
            return redirect('orders:track', token=token.strip())
        
        # Authenticated users manage orders in their history
        if request.user.is_authenticated:
            return redirect('orders:history')
            
        return render(request, 'orders/track.html')

    def post(self, request):
        token = request.POST.get('token')
        if token:
            return redirect('orders:track', token=token.strip())
            
        # Authenticated users manage orders in their history
        if request.user.is_authenticated:
            return redirect('orders:history')
            
        return render(request, 'orders/track.html', {'error': 'Por favor ingresa un código válido.'})
