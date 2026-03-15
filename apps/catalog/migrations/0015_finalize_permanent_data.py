from django.db import migrations

def finalize_catalog_data(apps, schema_editor):
    Flower = apps.get_model('catalog', 'Flower')
    Service = apps.get_model('catalog', 'Service')

    # 1. Update Flower Images (The logic from fix_flower_images.py)
    flowers_to_fix = [
        { 'name': 'Anémona', 'img': 'fotos sin fondo tallos/cayena/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/cayena/sin tallo/up.png' },
        { 'name': 'Lirio', 'img': 'fotos sin fondo tallos/lirios/tallo grande/frente.png', 'thumb': 'fotos sin fondo tallos/lirios/sin tallo/up.png' },
        { 'name': 'Girasol', 'img': 'fotos sin fondo tallos/girasoles/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/girasoles/sin tallo/up.png' },
        { 'name': 'Cayena', 'img': 'fotos sin fondo tallos/flor estrella/tallo grande/frente.png', 'thumb': 'fotos sin fondo tallos/flor estrella/sin tallo/up.png' },
        { 'name': 'Fantasía', 'img': 'fotos sin fondo tallos/flores de fantasia/tallos grandes/frente.png', 'thumb': 'fotos sin fondo tallos/flores de fantasia/sin tallo/up.png' },
        { 'name': 'Tulipán', 'img': 'fotos sin fondo tallos/tulipanes/tallos pequeños/frente.png', 'thumb': 'fotos sin fondo tallos/tulipanes/sin tallo/up.png' },
        { 'name': 'Flor Copo', 'img': 'fotos sin fondo tallos/flor copo/tallo pequeño/frente.png', 'thumb': 'fotos sin fondo tallo/flor copo/sin tallo/up.png' },
        { 'name': 'Normal', 'img': 'fotos sin fondo tallos/flores normales/tallos pequeños/frente.png', 'thumb': 'fotos sin fondo tallos/flores normales/sin tallo/up.png' }
    ]

    for f_data in flowers_to_fix:
        Flower.objects.filter(name=f_data['name']).update(
            image=f_data['img'],
            thumbnail=f_data['thumb']
        )

    # 2. Ensure Predefined Services are permanent (Logic from 0014)
    services = [
        {
            'title': 'Peluches',
            'description': 'Acompaña tu ramo con un tierno peluche seleccionado especialmente para sorprender.',
            'icon': '🧸',
            'price': 15.00,
            'is_active': True,
            'order': 1
        },
        {
            'title': 'Notas y Tarjetas',
            'description': 'Agrega una nota escrita a mano con tu mensaje personalizado.',
            'icon': '✏️',
            'price': 2.50,
            'is_active': True,
            'order': 2
        },
        {
            'title': 'Envío a Domicilio',
            'description': 'Entregamos tus flores con el mayor cuidado en toda la ciudad.',
            'icon': '🚚',
            'price': 5.00,
            'is_active': True,
            'order': 3
        },
        {
            'title': 'WhatsApp Directo',
            'description': 'Recibe confirmación y seguimiento de tu pedido directamente por mensajería.',
            'icon': '💬',
            'price': 0.00,
            'is_active': True,
            'order': 4
        }
    ]

    for s_data in services:
        Service.objects.update_or_create(
            title=s_data['title'],
            defaults={
                'description': s_data['description'],
                'icon': s_data['icon'],
                'price': s_data['price'],
                'is_active': s_data['is_active'],
                'order': s_data['order']
            }
        )

def reverse_finalize(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0014_seed_services'),
    ]

    operations = [
        migrations.RunPython(finalize_catalog_data, reverse_code=reverse_finalize),
    ]
