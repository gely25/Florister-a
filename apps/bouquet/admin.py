from django.contrib import admin
from .models import Bouquet, BouquetItem

class BouquetItemInline(admin.TabularInline):
    model = BouquetItem
    extra = 0

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'total_price', 'created_at')
    inlines = [BouquetItemInline]
