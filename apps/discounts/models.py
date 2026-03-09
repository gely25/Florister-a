from django.db import models

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('global', 'Global (Toda la tienda)'),
        ('category', 'Por Categoría de Flor'),
        ('product', 'Por Flor Específica'),
        ('bouquet', 'Por Ramo Específico'),
        ('promotion', 'Por Promoción Específica'),
        ('service', 'Por Servicio Específico'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nombre del Descuento")
    type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='global', verbose_name="Tipo de Aplicación")
    
    # Target filters
    tier_target = models.CharField(max_length=1, choices=[('l','Grande'),('m','Mediana'),('s','Pequeña')], null=True, blank=True, verbose_name="Categoría Objetivo")
    flower_target = models.ForeignKey('catalog.Flower', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Flor Objetivo")
    bouquet_target = models.ForeignKey('catalog.PreDesignedBouquet', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ramo Objetivo")
    promotion_target = models.ForeignKey('catalog.Promotion', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Promoción Objetivo")
    service_target = models.ForeignKey('catalog.Service', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Servicio Objetivo")

    percentage = models.PositiveIntegerField(default=0, verbose_name="Porcentaje (%)", help_text="Ej: 15 para un 15 por ciento de descuento.")
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Fijo ($)", help_text="Ej: 5.00 para descontar 5 dólares exactos.")
    
    valid_from = models.DateTimeField(verbose_name="Válido desde")
    valid_to = models.DateTimeField(verbose_name="Válido hasta")
    is_active = models.BooleanField(default=True, verbose_name="Está activo")

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.percentage > 0 and self.fixed_amount > 0:
            raise ValidationError("Debe elegir entre un Porcentaje O un Monto Fijo, no ambos al mismo tiempo para evitar confusión en el cálculo.")
        if self.percentage == 0 and self.fixed_amount == 0:
            raise ValidationError("Debe ingresar ya sea un Porcentaje mayor a 0 o un Monto Fijo mayor a 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
