from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f"DEBUG BACKEND: Attempting auth for username={repr(username)}")
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # Try to fetch the user by username or email
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            print(f"DEBUG BACKEND: Found user in DB: {user.username}")
        except User.DoesNotExist:
            print("DEBUG BACKEND: User not found in DB")
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            print("DEBUG BACKEND: Multiple users found, taking first")
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            print("DEBUG BACKEND: Authentication SUCCESS")
            return user
        print("DEBUG BACKEND: Authentication FAILED (password mismatch or user inactive)")
        return None
