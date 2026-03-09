# Sisart — Sistema de Gestión de Floristería

Este proyecto es una plataforma integral para la gestión de una floristería, permitiendo a los clientes diseñar ramos personalizados, comprar productos del catálogo y rastrear sus pedidos, mientras que los vendedores administran el inventario y las ventas.

## ✨ Tecnologías de Animación e Interactividad

El dinamismo del sistema se logra mediante tres capas tecnológicas principales:

1.  **Intersection Observer API**: Implementada en el archivo base [base.html](file:///c:/SistemaFlores/templates/layouts/base.html#L155-L163) para efectos de "Scroll Reveal" (aparición suave al desplazar la página).
2.  **CSS Transitions & Keyframes**: 
    - Animaciones de entrada (ej: `fly`) y transiciones de estado en el diseñador [designer.html](file:///c:/SistemaFlores/apps/bouquet/templates/bouquet/designer.html).
    - Efectos hover premium en botones y tarjetas a lo largo de todo el sitio.
3.  **Lógica de Transformación Matemática (JS)**: El archivo [script.js](file:///c:/SistemaFlores/static/js/script.js#L269-L276) gestiona el motor de diseño, calculando en tiempo real las coordenadas (X, Y), escalas y rotaciones de cada flor mediante manipulación del DOM y CSS Variables.
4.  **Lucide Icons**: Integración de iconos vectoriales ligeros que se renderizan dinámicamente.

---

## 🛡️ Estrategias de Seguridad (Ubicación en Código)

El sistema implementa seguridad proactiva en puntos específicos del código:

### 1. Protección a Nivel de Middleware
- **Configuración Core**: En [settings.py](file:///c:/SistemaFlores/config/settings.py#L51-L59), se activan los middlewares contra CSRF, XSS y Clickjacking.
- **Cabeceras de Seguridad**: Se han implementado `SECURE_CONTENT_TYPE_NOSNIFF = True` y `X_FRAME_OPTIONS = "DENY"` en [settings.py](file:///c:/SistemaFlores/config/settings.py#L63-L64) para prevenir la inyección de tipos de contenido y ataques de clickjacking avanzados.

### 2. Control de Acceso Granular (Mixins e IDOR)
- **`SellerRequiredMixin`**: Ubicado en [apps/catalog/views.py](file:///c:/SistemaFlores/apps/catalog/views.py#L9-L11). Bloquea el acceso a funciones administrativas.
- **Protección IDOR**: La vista [OrderDetailView](file:///c:/SistemaFlores/apps/orders/views.py#L100) utiliza tokens únicos (UUID) para el seguimiento. Además, implementa una validación cruzada: si un usuario está autenticado, solo puede ver pedidos que le pertenecen o si es personal autorizado (staff).

### 3. Integridad y Privacidad
- **Variables de Entorno**: Carga segura de secretos en `settings.py` [L19](file:///c:/SistemaFlores/config/settings.py#L19).
- **Protección contra Manipulación de Precios**: El sistema ignora el precio enviado por el frontend. En [orders/services.py](file:///c:/SistemaFlores/apps/orders/services.py#L65), el precio final se calcula exclusivamente con los valores almacenados en la base de datos al momento de crear el pedido.
- **Login Seguro**: El sistema utiliza mensajes de error genéricos ("Credenciales incorrectas") en [login.html](file:///c:/SistemaFlores/templates/registration/login.html#L147) para evitar la enumeración de usuarios.
- **Sanitización de WhatsApp**: Uso de `encodeURIComponent()` en [script.js](file:///c:/SistemaFlores/static/js/script.js#L530) para evitar que caracteres especiales rompan el enlace.

### 4. Recomendaciones de Seguridad Futura
- **Fuerza Bruta**: Se recomienda implementar `django-ratelimit` en la vista de login para limitar intentos fallidos por IP (ej: máximo 5 por minuto).
- **Entorno de Producción**: Asegurarse de que `DEBUG = False`, configurar SSL completo y habilitar `SECURE_SSL_REDIRECT`.

---

## 🚦 Verificación y Validación de Pedidos

Es importante destacar que el sistema utiliza **WhatsApp únicamente como canal de contacto inicial**. 

> [!IMPORTANT]
> Todos los pedidos recibidos vía WhatsApp **son verificados manualmente por el vendedor** antes de su preparación. Esto mitiga riesgos de manipulación manual del precio o del contenido del pedido por parte de usuarios malintencionados en el enlace de la URL.

---

## 🏗️ Estructura del Sistema (Mapa de Archivos)

El sistema se organiza en módulos (apps) independientes:

### Core (`config/`)
- `settings.py`: Configuración global y seguridad.
- `urls.py`: Enrutador principal del sistema.

### Aplicaciones (`apps/`)
- **`accounts/`**: Modelo de usuario y gestión de perfiles.
- **`catalog/`**: Inventario de flores, tamaños de ramos y productos.
- **`bouquet/`**: Lógica del diseñador interactivo de ramos.
- **`dahsboard/`**: Paneles de control para clientes y vendedores.
- **`orders/`**: Gestión de pedidos, tracking y generación de mensajes de WhatsApp.
- **`discounts/`**: Sistema de cupones y promociones.

---

## 🔄 Flujo del Sistema (Resumen Ejecutivo)

1.  **Descubrimiento**: El usuario ingresa a la `Home`, explora el catálogo de productos y ramos predefinidos.
2.  **Identificación**: El usuario se registra o inicia sesión para habilitar funciones interactivas.
3.  **Personalización**: 
    - En el `Bouquet Designer`, el usuario selecciona un tamaño. El sistema valida las restricciones mínimas.
    - El usuario diseña su ramo visualmente ajustando flores, posiciones y giros.
4.  **Transacción**: El usuario procede al pago. El sistema genera una orden, asigna un `tracking_token` único y facilita el envío de datos vía WhatsApp al vendedor.
5.  **Gestión y Seguimiento**:
    - El **Cliente** ve su progreso en el `Dashboard`.
    - El **Vendedor** gestiona los estados del pedido desde su tablero administrativo.

---
© 2026 Sisart — Detalles que duran para siempre.
