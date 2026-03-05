from django.db import models

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('global', 'Global (Toda la tienda)'),
        ('category', 'Por Categoría de Flor'),
        ('product', 'Por Flor Específica'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='global')
    
    # Target filters
    tier_target = models.CharField(max_length=1, choices=[('l','Grande'),('m','Mediana'),('s','Pequeña')], null=True, blank=True)
    flower_target = models.ForeignKey('catalog.Flower', on_delete=models.CASCADE, null=True, blank=True)

    percentage = models.PositiveIntegerField(default=0)
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"
