from django import template
from apps.discounts.services import get_discounted_price_info

register = template.Library()

@register.simple_tag
def get_discount_info(obj):
    """
    Returns the discount information for a Flower or PreDesignedBouquet.
    Usage in template:
    {% get_discount_info product as discount %}
    {% if discount.has_discount %}
       ...
    {% endif %}
    """
    if not obj:
        return None
    return get_discounted_price_info(obj)
