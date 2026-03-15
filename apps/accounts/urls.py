from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, UserProfileUpdateView, check_username, check_email, AjaxLoginView, VerifyEmailView
from .forms import CustomPasswordResetForm

app_name = 'accounts'

urlpatterns = [
    path('login/', AjaxLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='signup'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='perfil_update'),
    path('check-username/', check_username, name='check_username'),
    path('check-email/', check_email, name='check_email'),

    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', 
                                              email_template_name='registration/password_reset_email.html',
                                              subject_template_name='registration/password_reset_subject.txt',
                                              success_url='/accounts/password-reset/done/',
                                              form_class=CustomPasswordResetForm), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                     success_url='/accounts/password-reset-complete/'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

    # Email Verification
    path('verification-sent/', 
         auth_views.TemplateView.as_view(template_name='registration/verification_sent.html'), 
         name='verification_sent'),
    path('verify-email/<uidb64>/<token>/', 
         VerifyEmailView.as_view(), 
         name='verify_email'),
]
