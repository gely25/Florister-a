from django.db import migrations

def seed_base_data(apps, schema_editor):
    BouquetSize = apps.get_model('catalog', 'BouquetSize')
    Flower = apps.get_model('catalog', 'Flower')

    # Seed Bouquet Sizes
    sizes = [
        {'name': 'Grande', 'code': 'grande', 'max_large': 3, 'max_medium': 3, 'max_small': 3, 'base_price': 45.00},
        {'name': 'Mediano', 'code': 'mediano', 'max_large': 3, 'max_medium': 2, 'max_small': 3, 'base_price': 35.00},
        {'name': 'Pequeño', 'code': 'pequeño', 'max_large': 1, 'max_medium': 2, 'max_small': 2, 'base_price': 25.00},
        {'name': 'Personalizado', 'code': 'personalizado', 'max_large': 4, 'max_medium': 4, 'max_small': 4, 'base_price': 0.00},
    ]

    for s_data in sizes:
        BouquetSize.objects.update_or_create(code=s_data['code'], defaults=s_data)

    # Seed Basic Flower records (without images to avoid path errors during migration)
    flowers = [
        { 'name': 'Anémona', 'tier': 'l', 'price': 15.00 },
        { 'name': 'Lirio', 'tier': 'l', 'price': 14.00 },
        { 'name': 'Girasol', 'tier': 'l', 'price': 12.00 },
        { 'name': 'Cayena', 'tier': 'm', 'price': 10.00 },
        { 'name': 'Fantasía', 'tier': 'm', 'price': 8.00 },
        { 'name': 'Tulipán', 'tier': 's', 'price': 7.00 },
        { 'name': 'Flor Copo', 'tier': 's', 'price': 6.00 },
        { 'name': 'Normal', 'tier': 's', 'price': 6.00 }
    ]

    for f_data in flowers:
        Flower.objects.get_or_create(
            name=f_data['name'],
            tier=f_data['tier'],
            defaults={'price': f_data['price']}
        )

def remove_base_data(apps, schema_editor):
    # Optional: logic to reverse this if needed, 
    # but usually we want to keep base data.
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0012_update_personalizado_limits'),
    ]

    operations = [
        migrations.RunPython(seed_base_data, reverse_code=remove_base_data),
    ]
