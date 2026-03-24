from .base import *

# Inyectar WhiteNoise solo en producción (después de SecurityMiddleware)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# En producción DEBUG temporalmente activo para diagnóstico
DEBUG = True
ALLOWED_HOSTS = ['*']

# Static files con whitenoise comprimidos, Media files en Cloudinary
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Configuración de Anymail para usar API de Brevo en la nube (salta el bloqueo SMTP port 587 de Render)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY", default=""),
}