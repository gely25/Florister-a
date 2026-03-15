from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .forms import UserSignUpForm, UserProfileUpdateForm
from .models import User

class AjaxLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'redirect_url': self.get_success_url()
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')
            print(f"DEBUG: Login failed for user (repr): {repr(username)}")
            print(f"DEBUG: Password length: {len(password) if password else 0}")
            print(f"DEBUG: Form errors: {form.errors.as_json()}")
            return JsonResponse({
                'status': 'error',
                'errors': form.errors.get_json_data()
            }, status=400)
        return super().form_invalid(form)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.views import View
from django.shortcuts import redirect, render

class SignUpView(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:verification_sent')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account until it is confirmed
        user.save()

        # Send verification email
        current_site = get_current_site(self.request)
        subject = 'Activa tu cuenta en Sisart'
        message = render_to_string('registration/verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        
        email = EmailMessage(subject, message, to=[user.email])
        email.send()
        
        return redirect(self.success_url)

class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            messages.success(request, "¡Tu correo ha sido verificado! Ya puedes iniciar sesión.")
            return redirect('accounts:login')
        else:
            return render(request, 'registration/verification_invalid.html')

from django.http import JsonResponse

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('dahsboard:client_dashboard')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Tu perfil ha sido actualizado correctamente.")
        return super().form_valid(form)

def check_username(request):
    username = request.GET.get('username', None)
    if username is None or username.strip() == '':
        return JsonResponse({'is_taken': False})
    data = {'is_taken': User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)

def check_email(request):
    email = request.GET.get('email', None)
    if email is None or email.strip() == '':
        return JsonResponse({'is_taken': False})
    data = {'is_taken': User.objects.filter(email__iexact=email).exists()}
    return JsonResponse(data)
