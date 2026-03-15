import os
import django

# Setup Django BEFORE importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.views import PasswordResetView
from django.test import override_settings

User = get_user_model()
email = 'samsgo25@gmail.com'

def test_password_reset():
    print(f"Testing password reset for: {email}")
    
    # Ensure user exists
    if not User.objects.filter(email=email).exists():
        print(f"User with email {email} not found. Creating temporary user.")
        User.objects.create_user(username='testreset', email=email, password='TemporaryPassword123!')

    # Trigger password reset with locmem backend
    with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
        factory = RequestFactory()
        request = factory.post(reverse('accounts:password_reset'), {'email': email})
        
        view = PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/accounts/password-reset/done/'
        )
        
        response = view(request)
        print(f"Response status: {response.status_code} (Should be 302)")
        
        print(f"Emails in outbox: {len(mail.outbox)}")
        if mail.outbox:
            sent_email = mail.outbox[0]
            print(f"Subject: {sent_email.subject.strip()}")
            if '/accounts/password-reset-confirm/' in sent_email.body:
                print("SUCCESS: Reset link found in email!")
                print("Email body looks correct.")
            else:
                print("FAILURE: Reset link not found in email.")
        else:
            print("FAILURE: No emails sent.")

if __name__ == "__main__":
    test_password_reset()
