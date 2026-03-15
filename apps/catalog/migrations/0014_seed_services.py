from django.db import migrations

def seed_services(apps, schema_editor):
    Service = apps.get_model('catalog', 'Service')
    
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

def remove_services(apps, schema_editor):
    Service = apps.get_model('catalog', 'Service')
    titles = ['Peluches', 'Notas y Tarjetas', 'Envío a Domicilio', 'WhatsApp Directo']
    Service.objects.filter(title__in=titles).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0013_seed_base_data'),
    ]

    operations = [
        migrations.RunPython(seed_services, reverse_code=remove_services),
    ]
