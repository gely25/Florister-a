from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, UserProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='signup'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='perfil_update'),
]
