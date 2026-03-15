from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User

class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if not any(c.isupper() for c in password):
                raise forms.ValidationError("La contraseña debe incluir al menos una mayúscula.")
            if not any(c.islower() for c in password):
                raise forms.ValidationError("La contraseña debe incluir al menos una minúscula.")
            if not any(c.isdigit() for c in password):
                raise forms.ValidationError("La contraseña debe incluir al menos un número.")
            if not any(not c.isalnum() for c in password):
                raise forms.ValidationError("La contraseña debe incluir al menos un símbolo (ej: !@#$%^&*).")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(max_length=254, required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("No hay ninguna cuenta activa registrada con este correo electrónico.")
        return email
