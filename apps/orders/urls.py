from django.urls import path
from .api.views import OrderCreateView, TrackOrderStubView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create'),
    path('track/<str:token>/', TrackOrderStubView.as_view(), name='track_order'),
]
