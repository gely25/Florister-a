import os
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.catalog.models import BouquetSize, Flower

class Command(BaseCommand):
    help = 'Populates the database with essential flowers and bouquet sizes'

    def handle(self, *args, **options):
        self.stdout.write("Populating BouquetSize...")
        sizes = [
            {'name': 'Grande', 'code': 'grande', 'max_large': 3, 'max_medium': 3, 'max_small': 3, 'base_price': 45.00},
            {'name': 'Mediano', 'code': 'mediano', 'max_large': 3, 'max_medium': 2, 'max_small': 3, 'base_price': 35.00},
            {'name': 'Pequeño', 'code': 'pequeño', 'max_large': 1, 'max_medium': 2, 'max_small': 2, 'base_price': 25.00},
            {'name': 'Personalizado', 'code': 'personalizado', 'max_large': 15, 'max_medium': 15, 'max_small': 20, 'base_price': 0.00},
        ]
        
        for s_data in sizes:
            obj, created = BouquetSize.objects.get_or_create(code=s_data['code'], defaults=s_data)
            if not created:
                for key, value in s_data.items():
                    setattr(obj, key, value)
                obj.save()
            self.stdout.write(f" - {'Created' if created else 'Updated'} size: {obj.name}")

        self.stdout.write("\nPopulating Flowers...")
        base_media = 'media/fotos sin fondo tallos/'
        flowers_to_import = [
            { 'name': 'Anémona', 'tier': 'l', 'price': 15.00, 'img': 'cayena/tallos grandes/frente.png', 'thumb': 'cayena/sin tallo/up.png' },
            { 'name': 'Lirio', 'tier': 'l', 'price': 14.00, 'img': 'lirios/tallo grande/frente.png', 'thumb': 'lirios/sin tallo/up.png' },
            { 'name': 'Girasol', 'tier': 'l', 'price': 12.00, 'img': 'girasoles/tallos grandes/frente.png', 'thumb': 'girasoles/sin tallo/up.png' },
            { 'name': 'Cayena', 'tier': 'm', 'price': 10.00, 'img': 'flor estrella/tallo grande/frente.png', 'thumb': 'flor estrella/sin tallo/up.png' },
            { 'name': 'Fantasía', 'tier': 'm', 'price': 8.00, 'img': 'flores de fantasia/tallos grandes/frente.png', 'thumb': 'flores de fantasia/sin tallo/up.png' },
            { 'name': 'Tulipán', 'tier': 's', 'price': 7.00, 'img': 'tulipanes/tallos pequeños/frente.png', 'thumb': 'tulipanes/sin tallo/up.png' },
            { 'name': 'Flor Copo', 'tier': 's', 'price': 6.00, 'img': 'flor copo/tallo pequeño/frente.png', 'thumb': 'flor copo/sin tallo/up.png' },
            { 'name': 'Normal', 'tier': 's', 'price': 6.00, 'img': 'flores normales/tallos pequeños/frente.png', 'thumb': 'flores normales/sin tallo/up.png' }
        ]

        for f_data in flowers_to_import:
            img_path = os.path.join(base_media, f_data['img'])
            thumb_path = os.path.join(base_media, f_data['thumb'])
            
            if not os.path.exists(img_path) or not os.path.exists(thumb_path):
                self.stdout.write(self.style.WARNING(f" ! Skipping {f_data['name']}: Files not found at {img_path}"))
                continue

            flower, created = Flower.objects.get_or_create(
                name=f_data['name'],
                tier=f_data['tier'],
                defaults={'price': f_data['price']}
            )
            
            with open(img_path, 'rb') as f_img:
                flower.image.save(os.path.basename(img_path), File(f_img), save=False)
            with open(thumb_path, 'rb') as f_thumb:
                flower.thumbnail.save(os.path.basename(thumb_path), File(f_thumb), save=False)
            
            flower.price = f_data['price']
            flower.save()
            self.stdout.write(f" - {'Created' if created else 'Updated'} flower: {flower.name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded bouquet data.'))
