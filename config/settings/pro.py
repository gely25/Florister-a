from .base import *
import os

# para collectstatic en producción
STATIC_ROOT= BASE_DIR / "staticfiles"  
#en producción no queremos que las imagenes se guarden el código
media_root = ""
DEBUG = False
DATABASES= { 'default': env.db(),} 