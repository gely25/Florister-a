from django import forms
from .models import Discount

class DiscountForm(forms.ModelForm):
    discount_method = forms.ChoiceField(
        choices=[('percentage', 'Porcentaje (%)'), ('fixed', 'Monto Fijo ($)')],
        label="Método de Descuento",
        required=True,
        initial='percentage'
    )

    class Meta:
        model = Discount
        fields = ['name', 'type', 'tier_target', 'flower_target', 'bouquet_target', 'promotion_target', 'service_target', 'discount_method', 'percentage', 'fixed_amount', 'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # The model's clean() will be called by the form, but let's double check if we need custom form logic
        return cleaned_data
