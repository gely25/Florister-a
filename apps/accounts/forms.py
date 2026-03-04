from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(max_length=254, required=True, help_text='Requerido para el seguimiento de tus pedidos.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.role = User.CUSTOMER # Default role for registration
        if commit:
            user.save()
        return user
