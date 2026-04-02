import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from apps.orders.services import _generate_bouquet_image_pillow
from apps.bouquet.models import Bouquet, BouquetSize

# Create a mock order structure
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
    print("Result:", res)
    if res:
        print("Generated file size:", len(res[1].read()))
except Exception as e:
    import traceback
    traceback.print_exc()

# Let's directly test the wrapper function to see why it fails
from PIL import Image, ImageColor, ImageChops
from django.conf import settings

def test_wrapper_alone():
    texture_path = os.path.join(settings.MEDIA_ROOT, "envoltura.png")
    if not os.path.exists(texture_path):
        texture_path = os.path.join(settings.BASE_DIR, "media", "envoltura.png")
        
    print("TEXTURE_PATH:", texture_path)
    print("EXISTS:", os.path.exists(texture_path))
    if os.path.exists(texture_path):
        try:
            texture = Image.open(texture_path).convert('RGBA')
            rgb = ImageColor.getrgb("#e8dfcc")
            print("RGB:", rgb)
            color_layer = Image.new('RGBA', texture.size, rgb + (255,))
            mult_rgb = ImageChops.multiply(texture.convert('RGB'), color_layer.convert('RGB'))
            result = mult_rgb.convert('RGBA')
            result.putalpha(texture.getchannel('A'))
            print("Wrap alpha channel set. Result size:", result.size)
        except Exception as e:
            print("EXCEPTION IN PIL:", e)
test_wrapper_alone()
