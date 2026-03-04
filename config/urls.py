from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.catalog.views import HomeView
from apps.orders.api.views import TrackOrderStubView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('bouquet/', include('apps.bouquet.urls')),
    path('orders/', include('apps.orders.urls')),
    path('dashboard/', include('apps.dahsboard.urls')),
    # Alias for old tracking links sent via WhatsApp
    path('pedidos/seguimiento/<str:token>/', TrackOrderStubView.as_view(), name='track_alias'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
