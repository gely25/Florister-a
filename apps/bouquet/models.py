from django.db import models
from apps.catalog.models import Flower, BouquetSize

class Bouquet(models.Model):
    size = models.ForeignKey(BouquetSize, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Ramo {self.size.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class BouquetItem(models.Model):
    bouquet = models.ForeignKey(Bouquet, related_name='items', on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.PROTECT)
    
    # Transformation and position data from frontend
    x = models.FloatField()
    y = models.FloatField()
    scale = models.FloatField(default=1.0)
    rotation = models.FloatField(default=0.0)
    
    # Price snapshotted at time of order
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flower.name} in Bouquet {self.bouquet.id}"
