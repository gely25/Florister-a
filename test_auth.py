import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import authenticate
from apps.accounts.models import User
from django.db.models import Q

def test_auth():
    username = 'ang'
    password = 'Ang12345!'
    
    print(f"Testing for user: {username}")
    
    # 1. Manual check
    try:
        user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        print(f"Found user: {user.username}, Email: {user.email}, Is Active: {user.is_active}")
        print(f"Password matches: {user.check_password(password)}")
    except User.DoesNotExist:
        print("User not found in DB via Q lookup")
    except Exception as e:
        print(f"Error lookup: {e}")

    # 2. Django authenticate check
    try:
        auth_user = authenticate(username=username, password=password)
        print(f"Django authenticate(username='{username}') result: {auth_user}")
        
        email_auth = authenticate(username=user.email, password=password)
        print(f"Django authenticate(username='{user.email}') result: {email_auth}")
    except Exception as e:
        print(f"Error authenticate: {e}")

if __name__ == "__main__":
    test_auth()
