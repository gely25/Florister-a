import os

# - Render (produccion): usa pro.py por defecto
# - Local: pon DJANGO_ENV=local en tu .env para usar local.py
env = os.environ.get('DJANGO_ENV', 'production')

if env == 'local':
    from .local import *
else:
    from .pro import *