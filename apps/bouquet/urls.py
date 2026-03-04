from django.urls import path
from .views import BouquetDesignView

app_name = 'bouquet'

urlpatterns = [
    path('design/', BouquetDesignView.as_view(), name='design'),
]
