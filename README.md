# Sisart — Sistema de Gestión de Floristería

Este proyecto es una plataforma integral para la gestión de una floristería, permitiendo a los clientes diseñar ramos personalizados y comprar productos, mientras que los vendedores administran el inventario y las ventas.

## 🔄 Flujo del Sistema

1.  **Exploración**: El usuario navega por la página de inicio pública para ver productos destacados y servicios.
2.  **Registro/Acceso**: Para realizar pedidos o usar el diseñador, el usuario debe identificarse.
3.  **Personalización y Pedido**:
    - **Catálogo**: Compra de ramos predefinidos o flores sueltas.
    - **Diseñador**: Creación visual de un ramo desde cero con selección de tamaño y flores.
4.  **Confirmación vía WhatsApp**: Al finalizar el diseño o selección, se genera un enlace de WhatsApp con todos los detalles técnicos para el vendedor.
5.  **Seguimiento**: Los usuarios pueden rastrear el estado de su pedido mediante un token único de seguimiento.

## 🖼️ Interfaces Principales

-   **Página de Inicio (Landing)**: Banners, catálogo destacado y servicios.
-   **Dashboard de Cliente**: Historial de pedidos y acceso directo al catálogo de cliente.
-   **Dashboard de Vendedor**: Resumen de ventas, gestión de stock de flores, edición de productos y control de estados de pedidos.
-   **Diseñador de Ramos**: Lienzo interactivo para posicionamiento, escala y rotación de flores.

## 🏗️ División del Proyecto (Apps)

El sistema se organiza en aplicaciones Django desacopladas:

-   **`accounts/`**: Gestión de usuarios personalizados (Roles: Vendedor vs Cliente).
-   **`catalog/`**: Modelos de Flores, Ramos Predefinidos, Tamaños y Servicios.
-   **`bouquet/`**: Motor del diseñador visual e interfaz de creación.
-   **`orders/`**: Lógica de creación de pedidos, tracking y generación de mensajes.
-   **`discounts/`**: sistema de promociones aplicables a productos.
-   **`dahsboard/`**: Vistas de administración y perfiles de usuario.

## 💻 Tecnologías Utilizadas

-   **Backend**: Python 3.12 + Django 6.0
-   **Base de Datos**: SQLite (Desarrollo) / Compatible con PostgreSQL (Producción).
-   **Frontend**: HTML5, Vanilla CSS3 (Modern UI), JavaScript ES6.
-   **Iconografía**: Lucide Icons.
-   **Procesamiento de Imágenes**: Pillow (PIL).
-   **Interconectividad**: API de WhatsApp Business (formato URL).
