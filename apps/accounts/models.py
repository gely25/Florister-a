from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    SELLER = 'seller'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (SELLER, 'Vendedor'),
        (CUSTOMER, 'Cliente'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=CUSTOMER
    )
    is_email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def display_role(self):
        if self.is_superuser:
            return "Administrador"
        if self.role == self.SELLER:
            return "Vendedor"
        return "Cliente"

    @property
    def is_seller(self):
        """Returns True if the user has the SELLER role."""
        return self.role == self.SELLER

    @property
    def is_customer(self):
        """Returns True if the user has the CUSTOMER role."""
        return self.role == self.CUSTOMER
