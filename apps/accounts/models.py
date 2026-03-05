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

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.role = self.SELLER
        super().save(*args, **kwargs)

    @property
    def display_role(self):
        if self.is_superuser:
            return "Administrador"
        if self.is_staff:
            return "Vendedor"
        return "Cliente"

    @property
    def is_seller(self):
        """Only the shop owner (staff) is the seller."""
        return self.is_staff

    @property
    def is_customer(self):
        """Everyone else who registers is a customer."""
        return not self.is_staff and self.role == self.CUSTOMER
