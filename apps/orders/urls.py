from django.urls import path
from . import views
from .api.views import OrderCreateView
from .api.quick_order import QuickOrderCreateView

app_name = 'orders'

urlpatterns = [
    path('history/', views.OrderHistoryView.as_view(), name='history'),
    path('management/', views.OrderListView.as_view(), name='management_list'),
    path('management/<int:pk>/', views.OrderManagementDetailView.as_view(), name='management_detail'),
    path('management/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='update_status'),
    path('track/', views.TrackOrderSearchView.as_view(), name='track_search'),
    path('track/<str:token>/', views.OrderDetailView.as_view(), name='track'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('quick-order/', QuickOrderCreateView.as_view(), name='quick_order'),
]
