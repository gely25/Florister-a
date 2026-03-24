from .base import *

# Inyectar WhiteNoise solo en producción (después de SecurityMiddleware)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Usar almacenamiento comprimido pero no estricto con el manifiesto para evitar caídas
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT = False

# En producción DEBUG desactivado nuevamente
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.onrender.com'])

# Configuración de Anymail para usar API de Brevo en la nube (salta el bloqueo SMTP port 587 de Render)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY", default=""),
}