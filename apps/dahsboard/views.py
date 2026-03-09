from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_seller:
        return redirect('dahsboard:seller_dashboard')
    return redirect('dahsboard:client_catalog')

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
    
    # Real Order Data
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    total_orders_count = Order.objects.filter(user=request.user).count()
    
    # We could also fetch active coupons if relevant
    
    context = {
        'recent_orders': recent_orders,
        'total_orders_count': total_orders_count,
    }
    return render(request, 'dahsboard/client_dashboard.html', context)

@login_required
def promotions_view(request):
    if not request.user.is_customer:
        return redirect('dahsboard:index')
        
    from apps.discounts.services import get_discounted_price_info
    from apps.catalog.models import Flower, PreDesignedBouquet, Promotion, Service
    from django.core.paginator import Paginator
    
    search_query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '')
    
    # Base QuerySets
    flowers_qs = Flower.objects.filter(is_active=True)
    bouquets_qs = PreDesignedBouquet.objects.filter(is_active=True)
    promos_qs = Promotion.objects.filter(is_active=True)
    services_qs = Service.objects.filter(is_active=True)
    
    # Filter by name if search query is provided
    if search_query:
        flowers_qs = flowers_qs.filter(name__icontains=search_query)
        bouquets_qs = bouquets_qs.filter(name__icontains=search_query)
        promos_qs = promos_qs.filter(name__icontains=search_query)
        services_qs = services_qs.filter(title__icontains=search_query)
        
    discounted_items = []
    
    # 1. Flowers
    if not type_filter or type_filter == 'flower':
        for item in flowers_qs:
            info = get_discounted_price_info(item)
            if info['has_discount']:
                item.discount_info = info
                item.item_type = 'flower'
                discounted_items.append(item)
                
    # 2. Bouquets & Promotions (Combined as "Ramos" or products)
    if not type_filter or type_filter == 'bouquet':
        for item in list(bouquets_qs) + list(promos_qs):
            info = get_discounted_price_info(item)
            if info['has_discount']:
                item.discount_info = info
                item.item_type = 'bouquet'
                discounted_items.append(item)
                
    # 3. Services
    if not type_filter or type_filter == 'service':
        for item in services_qs:
            info = get_discounted_price_info(item)
            if info['has_discount']:
                item.discount_info = info
                item.item_type = 'service'
                discounted_items.append(item)
                
    # Pagination
    paginator = Paginator(discounted_items, 6) # 6 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'current_type': type_filter,
    }
    return render(request, 'dahsboard/promotions.html', context)

@login_required
def placeholder(request):
    return render(request, 'dahsboard/placeholder.html')

@login_required
def client_catalog_view(request):
    if not request.user.is_customer:
        return redirect('dahsboard:index')
        
    from apps.discounts.services import get_discounted_price_info
    from apps.catalog.models import Flower, PreDesignedBouquet
    
    search_query = request.GET.get('q', '').strip()
    
    # Fetch all active items
    flowers_qs = Flower.objects.filter(is_active=True)
    bouquets_qs = PreDesignedBouquet.objects.filter(is_active=True)
    
    if search_query:
        flowers_qs = flowers_qs.filter(name__icontains=search_query)
        bouquets_qs = bouquets_qs.filter(name__icontains=search_query)
        
    items = []
    
    # 1. Flowers
    for item in flowers_qs:
        item.discount_info = get_discounted_price_info(item)
        item.item_type = 'flower'
        items.append(item)
        
    # 2. Bouquets
    for item in bouquets_qs:
        item.discount_info = get_discounted_price_info(item)
        item.item_type = 'bouquet'
        items.append(item)
        
    context = {
        'items': items,
        'search_query': search_query,
    }
    return render(request, 'dahsboard/client_catalog.html', context)
