import os
import django
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def debug_email():
    print("--- Diagnostic Report ---")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    User = get_user_model()
    emails_to_check = ['samsgo25@gmail.com', 'sisarte8@gmail.com']
    
    for email in emails_to_check:
        count = User.objects.filter(email=email).count()
        print(f"Users with email {email}: {count}")
    
    print("\nAttempting to send a test email...")
    try:
        with mail.get_connection() as connection:
            mail.EmailMessage(
                'Test Sisart Diagnostic',
                'This is a diagnostic email to test SMTP settings.',
                settings.DEFAULT_FROM_EMAIL,
                [emails_to_check[0]],
                connection=connection,
            ).send()
        print("SUCCESS: Email sent successfully!")
    except Exception as e:
        print(f"FAILURE: Could not send email.")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")

if __name__ == "__main__":
    debug_email()
