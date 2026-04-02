import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from apps.orders.services import _generate_bouquet_image_pillow
from apps.bouquet.models import Bouquet
class MockBouquet:
    def __init__(self):
        self.items = MockManager()
class MockManager:
    def all(self):
        return self
    def select_related(self, *args):
        return []

try:
    m = MockBouquet()
    res = _generate_bouquet_image_pillow(m, 'test-123', {'color':'#e8dfcc', 'scale':1.0, 'x':0, 'y':0})
    if res:
        with open('test.jpg', 'wb') as f:
            f.write(res[1].read())
        print("SAVED to test.jpg")
except Exception as e:
    import traceback
    traceback.print_exc()
