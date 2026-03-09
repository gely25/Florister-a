from django.contrib import admin
from .models import Flower, BouquetSize, Service, Promotion, PortfolioItem, PreDesignedBouquet

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'price', 'is_active', 'is_featured')
    list_filter = ('tier', 'is_active', 'is_featured')

@admin.register(BouquetSize)
class BouquetSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'max_large', 'max_medium', 'max_small', 'base_price')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'order')
    list_editable = ('order', 'is_active')
@admin.register(PreDesignedBouquet)
class PreDesignedBouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'price', 'stock', 'is_active')
    list_filter = ('size', 'is_active')
