from .base import *
import os

# Configuración de almacenamiento en producción
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# MEDIA_ROOT se hereda de base.py (BASE_DIR / 'media')
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'florist_db',
        'USER': 'postgres',
        'PASSWORD': 'Admin25#',  
        'HOST': 'localhost',
        'PORT': '5432',
    }
}