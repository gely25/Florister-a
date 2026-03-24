from .base import *

# En producción DEBUG desactivado para seguridad
DEBUG = False

# Dominios permitidos en Render
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.onrender.com'])

# Static files con whitenoise comprimidos, Media files en Cloudinary
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

# Configuración de Anymail para usar API de Brevo en la nube (salta el bloqueo SMTP port 587 de Render)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY", default=""),
}