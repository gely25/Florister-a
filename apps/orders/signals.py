from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Order
from apps.catalog.models import Flower, PreDesignedBouquet

@receiver(post_save, sender=Order)
def handle_stock_on_status_change(sender, instance, created, **kwargs):
    """
    Automatically manage stock based on order status changes.
    - Confirmed: Decrement stock.
    - Cancelled (from a previously confirmed/active state): Restore stock.
    """
    if created and instance.status == 'pending':
        # Stock is not managed at creation for pending orders
        return

    old_status = instance.original_status
    new_status = instance.status

    if old_status == new_status:
        return

    # Statuses that imply stock is consumed
    ACTIVE_STATUSES = ['confirmed', 'preparing', 'ready', 'delivered']
    
    with transaction.atomic():
        # 1. Transition to Confirmed (Stock becomes reserved/consumed)
        if old_status == 'pending' and new_status == 'confirmed':
            _update_stock(instance, decrement=True)
            
        # 2. Transition from Active to Cancelled (Stock restored)
        elif old_status in ACTIVE_STATUSES and new_status == 'cancelled':
            _update_stock(instance, decrement=False)
            
        # 3. Transition from Cancelled back to Confirmed (Stock consumed again)
        elif old_status == 'cancelled' and new_status == 'confirmed':
            _update_stock(instance, decrement=True)

def _update_stock(order, decrement=True):
    """
    Helper to increment/decrement inventory.
    Handles custom bouquets (flowers) and pre-designed products.
    """
    multiplier = -1 if decrement else 1
    
    # Custom Bouquet: Flowers stock
    if order.bouquet and order.bouquet.items.exists():
        for item in order.bouquet.items.all():
            flower = item.flower
            flower.stock = max(0, flower.stock + multiplier)
            flower.save()
            
    # Pre-designed product: Bouquet stock
    if order.item_type == 'predesigned' and order.item_id:
        try:
            product = PreDesignedBouquet.objects.get(id=order.item_id)
            # Find quantity if stored, otherwise default to 1 for now
            # (Order model currently doesn't store quantity, assuming 1 for predesigned card clicks)
            # Note: quick_order logic used quantity=1 as default
            product.stock = max(0, product.stock + multiplier)
            product.save()
        except PreDesignedBouquet.DoesNotExist:
            pass
