import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default seller user for production initialization if none exists'

    def handle(self, *args, **options):
        # We look for a specific seller email and password in the env variable,
        # or use a default one for the seller user.
        email = os.environ.get('SELLER_EMAIL', 'sisarte8@gmail.com')
        password = os.environ.get('SELLER_PASSWORD', 'Sisart2026!')
        username = os.environ.get('SELLER_USERNAME', 'vendedor')

        # Check if the desired seller already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.SUCCESS(f'El vendedor {email} ya existe en la base de datos.'))
            return
            
        # Or if someone manually assigned the SELLER role to another user
        if User.objects.filter(role=User.SELLER).exists():
            self.stdout.write(self.style.WARNING('Ya existe un usuario con el rol de VENDEDOR. Asegurando consistencia...'))

        self.stdout.write('Creando usuario vendedor por defecto...')
        try:
            # We use is_staff=True so the seller can potentially access some generic panels if necessary,
            # but is_superuser=False to prevent total system control.
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=User.SELLER,
                is_staff=True,
                is_superuser=False,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'Vendedor creado con éxito: {email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear el vendedor: {str(e)}'))
