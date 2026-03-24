from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.catalog.views import HomeView
from apps.orders.views import OrderDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('bouquet/', include('apps.bouquet.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('discounts/', include('apps.discounts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('dashboard/', include('apps.dahsboard.urls')),
    # Alias for old tracking links sent via WhatsApp
    path('pedidos/seguimiento/<str:token>/', OrderDetailView.as_view(), name='track_alias'),
]

# El servicio de estáticos en producción lo maneja WhiteNoise
# El servicio de media en producción lo maneja Cloudinary
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
