def get_menu_for_user(user):
    """
    Returns a list of menu items based on the user's role.
    """
    from django.urls import reverse

    if not user.is_authenticated:
        return [
            {'name': 'Inicio', 'url': '/', 'icon': 'home'},
            {'name': 'Diseñador', 'url': reverse('bouquet:design'), 'icon': 'flower'},
        ]

    if user.is_seller:
        return [
            {'name': 'Catálogo', 'url': reverse('catalog:index'), 'icon': 'grid'},
            {'name': 'Resumen', 'url': reverse('dahsboard:seller_dashboard'), 'icon': 'layout-dashboard'},
            {'name': 'Gestión de Pedidos', 'url': reverse('orders:management_list'), 'icon': 'shopping-bag'},
            {'name': 'Inventario Flores', 'url': reverse('catalog:flower_list'), 'icon': 'flower-2'},
            {'name': 'Ramos Catálogo', 'url': reverse('catalog:predesigned_list'), 'icon': 'image'},
            {'name': 'Otros Servicios', 'url': reverse('catalog:service_list'), 'icon': 'settings'},
            {'name': 'Portafolio', 'url': reverse('catalog:portfolio_list'), 'icon': 'camera'},
            {'name': 'Descuentos y Promos', 'url': reverse('discounts:discount_list'), 'icon': 'tag'},
            {'name': 'Diseños Clientes', 'url': reverse('bouquet:bouquet_list'), 'icon': 'flower'},
        ]
    
    # Default is Customer
    return [
        {'name': 'Ver Catálogo', 'url': reverse('dahsboard:client_catalog'), 'icon': 'grid'},
        {'name': 'Resumen', 'url': reverse('dahsboard:client_dashboard'), 'icon': 'layout-dashboard'},
        {'name': 'Mis Pedidos', 'url': reverse('orders:history'), 'icon': 'history'},
        {'name': 'Diseña tu ramo', 'url': reverse('bouquet:design'), 'icon': 'flower'},
        {'name': 'Promociones', 'url': reverse('dahsboard:promotions_list'), 'icon': 'gift'},
    ]
