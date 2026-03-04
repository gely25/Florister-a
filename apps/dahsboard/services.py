def get_menu_for_user(user):
    """
    Returns a list of menu items based on the user's role.
    Each item is a dict with 'name', 'url', and 'icon'.
    """
    if not user.is_authenticated:
        return [
            {'name': 'Construir Ramo', 'url': '/bouquet/design/', 'icon': 'bouquet'},
            {'name': 'Login', 'url': '/accounts/login/', 'icon': 'login'},
        ]

    if user.is_seller():
        return [
            {'name': 'Gestión de Pedidos', 'url': '/dashboard/orders/', 'icon': 'shopping_bag'},
            {'name': 'Editor de Catálogo', 'url': '/dashboard/catalog/', 'icon': 'flower'},
            {'name': 'Descuentos', 'url': '/dashboard/discounts/', 'icon': 'tag'},
            {'name': 'Reportes', 'url': '/dashboard/reports/', 'icon': 'chart'},
        ]
    
    # Default is Customer
    return [
        {'name': 'Mi Perfil', 'url': '/accounts/profile/', 'icon': 'user'},
        {'name': 'Mis Pedidos', 'url': '/orders/history/', 'icon': 'history'},
        {'name': 'Nuevo Ramo', 'url': '/bouquet/design/', 'icon': 'plus'},
    ]
