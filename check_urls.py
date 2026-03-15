import os
import django
from django.urls import reverse, NoReverseMatch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def check_url(name):
    try:
        url = reverse(name)
        print(f"URL for '{name}': {url}")
    except NoReverseMatch as e:
        print(f"Error reversing '{name}': {e}")

print("Checking URLs...")
check_url('home')
check_url('catalog:home')
check_url('catalog:index')
