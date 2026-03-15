import os

# Determina qué archivo de configuración cargar
# Por defecto usa 'local', cámbialo a 'pro' en tu .env para producción
env_settings = os.getenv('DJANGO_SETTINGS_ENV', 'local')

if env_settings == 'pro':
    from .pro import *
else:
    from .local import *