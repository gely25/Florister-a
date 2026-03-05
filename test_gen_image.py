import os
import django
from decimal import Decimal
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order
from apps.orders.services import _generate_bouquet_image_pillow

def test_last_order():
    order = Order.objects.latest('id')
    print(f"Testing Order ID: {order.id}")
    print(f"Tracking Token: {order.tracking_token}")
    print(f"Bouquet items: {order.bouquet.items.count()}")
    
    # Mocking wrap_data if missing
    wrap_data = {'color': '#e8dfcc', 'scale': 1.0, 'x': 0, 'y': 0}
    
    try:
        result = _generate_bouquet_image_pillow(order.bouquet, str(order.tracking_token), wrap_data)
        if result:
            filename, content_file = result
            save_path = os.path.join("tmp", filename)
            if not os.path.exists("tmp"): os.makedirs("tmp")
            with open(save_path, "wb") as f:
                f.write(content_file.read())
            print(f"Image generated successfully at {save_path}")
            print(f"Size: {len(content_file)} bytes")
        else:
            print("Failed to generate image (None returned)")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_last_order()
