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

    def is_seller(self):
        return self.role == self.SELLER

    def is_customer(self):
        return self.role == self.CUSTOMER
