from django.db import models

class BouquetSize(models.Model):
    name = models.CharField(max_length=50) # Grande, Mediano, Pequeño, Personalizado
    code = models.SlugField(unique=True)
    max_large = models.PositiveIntegerField(default=0)
    max_medium = models.PositiveIntegerField(default=0)
    max_small = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Flower(models.Model):
    TIER_CHOICES = [
        ('l', 'Grande'),
        ('m', 'Mediana'),
        ('s', 'Pequeña'),
    ]
    
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=1, choices=TIER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100) # Added stock field
    image = models.ImageField(upload_to='flowers/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='flowers/thumbs/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_tier_display()})"

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Emoji o clase de icono (ej: 🧸, 💬)", blank=True, null=True)
    image_icon = models.ImageField(upload_to='service_icons/', null=True, blank=True, help_text="Imagen 3D o personaliza para el servicio")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class PortfolioItem(models.Model):
    title = models.CharField(max_length=100, blank=True, help_text="Opcional, de referencia interna")
    image = models.ImageField(upload_to='portfolio/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f"Portafolio #{self.id}"

    def save(self, *args, **kwargs):
        if not self.pk and self.order == 0:
            last_item = PortfolioItem.objects.all().order_by('-order').first()
            if last_item:
                self.order = last_item.order + 1
            else:
                self.order = 1
        super().save(*args, **kwargs)

class PreDesignedBouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pre-designed/')
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=50, default="Galería")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='promotions/')
    stars = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
