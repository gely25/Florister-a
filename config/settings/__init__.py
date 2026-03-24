import os

# Determina qué archivo de configuración cargar
# Por defecto usa 'pro' en servidores (Render) a menos que se especifique 'local'
is_on_render = os.getenv('RENDER') == 'true'
default_env = 'pro' if is_on_render else 'local'
env_settings = os.getenv('DJANGO_SETTINGS_ENV', default_env)

if env_settings == 'pro':
    from .pro import *
else:
    from .local import *