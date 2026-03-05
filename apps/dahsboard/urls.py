from django.urls import path
from . import views

app_name = 'dahsboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('coming-soon/', views.placeholder, name='placeholder'),
]
