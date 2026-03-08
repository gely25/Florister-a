from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogIndexView.as_view(), name='index'),
    # Flowers
    path('flowers/', views.FlowerListView.as_view(), name='flower_list'),
    path('flowers/add/', views.FlowerCreateView.as_view(), name='flower_create'),
    path('flowers/<int:pk>/edit/', views.FlowerUpdateView.as_view(), name='flower_update'),
    path('flowers/<int:pk>/delete/', views.FlowerDeleteView.as_view(), name='flower_delete'),
    
    # Services
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Pre-designed Bouquets
    path('predesigned/', views.PreDesignedBouquetListView.as_view(), name='predesigned_list'),
    path('predesigned/add/', views.PreDesignedBouquetCreateView.as_view(), name='predesigned_create'),
    path('predesigned/<int:pk>/edit/', views.PreDesignedBouquetUpdateView.as_view(), name='predesigned_update'),
    path('predesigned/<int:pk>/delete/', views.PreDesignedBouquetDeleteView.as_view(), name='predesigned_delete'),

    # Bulk Pricing
    path('flowers/update-prices/', views.BulkPriceUpdateView.as_view(), name='price_update'),

    # Portfolio
    path('portfolio/', views.PortfolioItemListView.as_view(), name='portfolio_list'),
    path('portfolio/add/', views.PortfolioItemCreateView.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/edit/', views.PortfolioItemUpdateView.as_view(), name='portfolio_update'),
    path('portfolio/<int:pk>/delete/', views.PortfolioItemDeleteView.as_view(), name='portfolio_delete'),
]
