from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_seller:
        return redirect('dahsboard:seller_dashboard')
    return redirect('dahsboard:client_dashboard')

from django.db.models import Sum
from django.utils import timezone
from apps.orders.models import Order
from apps.catalog.models import Flower, Service, PreDesignedBouquet

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('dahsboard:index')
    
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Metrics
    pending_orders_count = Order.objects.filter(status='pending').count()
    completed_today_count = Order.objects.filter(status='delivered', updated_at__gte=today_start).count()
    
    # Low Stock Alerts
    low_flowers = Flower.objects.filter(stock__lt=10).count()
    low_bouquets = PreDesignedBouquet.objects.filter(stock__lt=5).count()
    total_low_stock = low_flowers + low_bouquets

    # Sales Data
    total_sales_today = Order.objects.filter(status='delivered', updated_at__gte=today_start).aggregate(total=Sum('final_amount'))['total'] or 0
    
    # Recent Orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'pending_count': pending_orders_count,
        'completed_today': completed_today_count,
        'low_stock_count': total_low_stock,
        'sales_today': total_sales_today,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'dahsboard/seller_dashboard.html', context)

@login_required
def client_dashboard(request):
    if not request.user.is_customer:
        return redirect('dahsboard:index')
    return render(request, 'dahsboard/client_dashboard.html')

@login_required
def placeholder(request):
    return render(request, 'dahsboard/placeholder.html')
