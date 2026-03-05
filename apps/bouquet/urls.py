from django.urls import path
from . import views
from .views import BouquetDesignView

app_name = 'bouquet'

urlpatterns = [
    path('design/', BouquetDesignView.as_view(), name='design'),
    path('list/', views.BouquetListView.as_view(), name='bouquet_list'),
    path('<int:pk>/', views.BouquetDetailView.as_view(), name='bouquet_detail'),
    path('<int:pk>/delete/', views.BouquetDeleteView.as_view(), name='bouquet_delete'),
]
