from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserSignUpForm, UserProfileUpdateForm
from .models import User

class SignUpView(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'

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
