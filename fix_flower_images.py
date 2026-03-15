import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Flower

flowers_to_fix = [
    { 'name': 'Anémona', 'img': 'fotos sin fondo tallos/cayena/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/cayena/sin tallo/up.png' },
    { 'name': 'Lirio', 'img': 'fotos sin fondo tallos/lirios/tallo grande/frente.png', 'thumb': 'fotos sin fondo tallos/lirios/sin tallo/up.png' },
    { 'name': 'Girasol', 'img': 'fotos sin fondo tallos/girasoles/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/girasoles/sin tallo/up.png' },
    { 'name': 'Cayena', 'img': 'fotos sin fondo tallos/flor estrella/tallo grande/frente.png', 'thumb': 'fotos sin fondo tallos/flor estrella/sin tallo/up.png' },
    { 'name': 'Fantasía', 'img': 'fotos sin fondo tallos/flores de fantasia/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/flores de fantasia/sin tallo/up.png' },
    { 'name': 'Tulipán', 'img': 'fotos sin fondo tallos/tulipanes/tallos pequeños/frente.png', 'thumb': 'fotos sin fondo tallos/tulipanes/sin tallo/up.png' },
    { 'name': 'Flor Copo', 'img': 'fotos sin fondo tallos/flor copo/tallo pequeño/frente.png', 'thumb': 'fotos sin fondo tallos/flor copo/sin tallo/up.png' },
    { 'name': 'Normal', 'img': 'fotos sin fondo tallos/flores normales/tallos pequeños/frente.png', 'thumb': 'fotos sin fondo tallos/flores normales/sin tallo/up.png' }
]

for f_data in flowers_to_fix:
    try:
        flower = Flower.objects.get(name=f_data['name'])
        flower.image = f_data['img']
        flower.thumbnail = f_data['thumb']
        flower.save()
        print(f"Fixed images for: {flower.name}")
    except Flower.DoesNotExist:
        print(f"Flower {f_data['name']} not found.")
    except Exception as e:
        print(f"Error fixing {f_data['name']}: {str(e)}")
