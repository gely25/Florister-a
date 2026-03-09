from decimal import Decimal
from django.utils import timezone
from .models import Discount

def get_discounted_price_info(obj):
    """
    Calculates the best applicable discount for a Flower or PreDesignedBouquet.
    Returns a dict with:
    - original_price
    - final_price
    - discount_amount
    - discount_label (e.g., "15% OFF" or "$5 OFF")
    - has_discount (boolean)
    """
    from apps.catalog.models import Flower, PreDesignedBouquet, Promotion, Service
    
    now = timezone.now()
    original_price = obj.price
    best_final_price = original_price
    best_discount_amount = Decimal('0.00')
    discount_label = ""
    has_discount = False

    active_discounts = Discount.objects.filter(
        is_active=True, 
        valid_from__lte=now, 
        valid_to__gte=now
    )

    for d in active_discounts:
        current_discount = Decimal('0.00')
        current_label = ""
        
        # 1. Check Global
        if d.type == 'global':
            if d.percentage > 0:
                current_discount = (original_price * d.percentage) / 100
                current_label = f"{d.percentage}% OFF"
            else:
                current_discount = d.fixed_amount
                current_label = f"${d.fixed_amount} OFF"
        
        # 2. Check Category (only for Flowers)
        elif d.type == 'category' and isinstance(obj, Flower):
            if d.tier_target == obj.tier:
                if d.percentage > 0:
                    current_discount = (original_price * d.percentage) / 100
                    current_label = f"{d.percentage}% OFF"
                else:
                    current_discount = d.fixed_amount
                    current_label = f"${d.fixed_amount} OFF"
        
        # 3. Check Product (for Flowers)
        elif d.type == 'product' and isinstance(obj, Flower):
            if d.flower_target == obj:
                if d.percentage > 0:
                    current_discount = (original_price * d.percentage) / 100
                    current_label = f"{d.percentage}% OFF"
                else:
                    current_discount = d.fixed_amount
                    current_label = f"${d.fixed_amount} OFF"
        
        # 4. Check Bouquet Specific
        elif d.type == 'bouquet' and isinstance(obj, PreDesignedBouquet):
            if d.bouquet_target == obj:
                if d.percentage > 0:
                    current_discount = (original_price * d.percentage) / 100
                    current_label = f"{d.percentage}% OFF"
                else:
                    current_discount = d.fixed_amount
                    current_label = f"${d.fixed_amount} OFF"

        # 5. Check Promotion Specific
        elif d.type == 'promotion' and isinstance(obj, Promotion):
            if d.promotion_target == obj:
                if d.percentage > 0:
                    current_discount = (original_price * d.percentage) / 100
                    current_label = f"{d.percentage}% OFF"
                else:
                    current_discount = d.fixed_amount
                    current_label = f"${d.fixed_amount} OFF"

        # 6. Check Service Specific
        elif d.type == 'service' and isinstance(obj, Service):
            if d.service_target == obj:
                if d.percentage > 0:
                    current_discount = (original_price * d.percentage) / 100
                    current_label = f"{d.percentage}% OFF"
                else:
                    current_discount = d.fixed_amount
                    current_label = f"${d.fixed_amount} OFF"

        if current_discount > best_discount_amount:
            best_discount_amount = current_discount
            discount_label = current_label
            has_discount = True

    final_price = (original_price - best_discount_amount).quantize(Decimal('0.01'))
    if final_price < 0: final_price = Decimal('0.00')

    return {
        'original_price': original_price,
        'final_price': final_price,
        'discount_amount': best_discount_amount,
        'discount_label': discount_label,
        'has_discount': has_discount
    }
