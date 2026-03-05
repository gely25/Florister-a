import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT id FROM orders_order")
    ids = [row[0] for row in cursor.fetchall()]

for order_id in ids:
    new_uuid = str(uuid.uuid4())
    with connection.cursor() as cursor:
        cursor.execute("UPDATE orders_order SET tracking_token = %s WHERE id = %s", [new_uuid, order_id])
    print(f"Updated Order {order_id} with UUID {new_uuid}")
