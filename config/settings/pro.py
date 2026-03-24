from .base import *

# En producción DEBUG siempre desactivado
DEBUG = False

# Dominios permitidos: el de Render + dominio personalizado si tienes
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    '.onrender.com',
])

# CSRF: necesario para que los formularios funcionen en HTTPS
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'https://*.onrender.com',
])

# Seguridad HTTPS (Render termina TLS en el proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Opcional: Para evitar advertencias de Cloudinary en variables de entorno (aunque render las inyectará)
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': env('CLOUDINARY_URL')
}

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
