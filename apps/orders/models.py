from django.db import models
from django.conf import settings
from apps.bouquet.models import Bouquet
from apps.discounts.models import Coupon
import secrets

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    # Guest data if user is not logged in
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Guest and Auth Order Tracking and Image
    tracking_token = models.CharField(max_length=12, unique=True, db_index=True, blank=True)
    bouquet_image = models.ImageField(upload_to='orders/bouquets/', null=True, blank=True)
    
    bouquet = models.OneToOneField(Bouquet, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_token:
            self.tracking_token = secrets.token_hex(6).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"
