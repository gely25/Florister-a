from apps.dahsboard.services import get_menu_for_user

def menu_context(request):
    """
    Makes the dynamic menu available in all templates.
    """
    return {
        'side_menu': get_menu_for_user(request.user)
    }
