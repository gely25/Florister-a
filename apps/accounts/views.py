from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserSignUpForm

class SignUpView(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
