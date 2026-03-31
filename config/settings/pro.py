from .base import *

# Middleware explícito para asegurar que WhiteNoise sea el primero tras SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# En producción DEBUG desactivado
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.onrender.com', 'localhost', '127.0.0.1'])

# Static files comprimidos con fallback (no estricto)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True # Fallback por si collectstatic falla o es parcial


# Configuración de Anymail para usar API de Brevo en la nube (salta el bloqueo SMTP port 587 de Render)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY", default=""),
}