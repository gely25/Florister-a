from django.conf import settings
from apps.dahsboard.services import get_menu_for_user

def menu_context(request):
    """
    Makes the dynamic menu and global config available in all templates.
    """
    return {
        'side_menu': get_menu_for_user(request.user),
        'whatsapp_number': getattr(settings, 'WHATSAPP_NUMBER', ''),
    }
