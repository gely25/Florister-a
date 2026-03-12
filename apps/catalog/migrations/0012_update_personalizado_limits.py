from django.db import migrations


def update_personalizado_limits(apps, schema_editor):
    BouquetSize = apps.get_model('catalog', 'BouquetSize')
    BouquetSize.objects.filter(code='personalizado').update(
        max_large=15,
        max_medium=15,
        max_small=20,
    )


def reverse_personalizado_limits(apps, schema_editor):
    # Revert to previous defaults if needed (adjust as appropriate)
    BouquetSize = apps.get_model('catalog', 'BouquetSize')
    BouquetSize.objects.filter(code='personalizado').update(
        max_large=0,
        max_medium=0,
        max_small=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_remove_service_image_icon_service_image_and_more'),
    ]

    operations = [
        migrations.RunPython(update_personalizado_limits, reverse_personalizado_limits),
    ]
