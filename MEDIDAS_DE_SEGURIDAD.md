# Medidas de Seguridad — Sisart

El sistema Sisart ha sido diseñado con un enfoque preventivo para proteger la integridad del negocio y la privacidad de los usuarios.

## 🛡️ Técnicas Implementadas

### 1. Protección contra Ataques Comunes
-   **CSRF (Cross-Site Request Forgery)**: Django protege todos los formularios mediante tokens únicos obligatorios.
-   **XSS (Cross-Site Scripting)**: El motor de plantillas de Django escapa automáticamente todo el contenido dinámico. En JavaScript, se usa `encodeURIComponent()` para sanitizar datos enviados a APIs externas.
-   **Clickjacking**: Implementación de la cabecera `X-Frame-Options: DENY` para evitar que el sitio sea embebido en frames maliciosos.

### 2. Control de Acceso y Roles
-   **Modelos Personalizados**: Se utiliza un modelo `User` que hereda de `AbstractUser` para definir roles claros (`SELLER`, `CUSTOMER`).
-   **Mixins de Seguridad**: Las vistas administrativas utilizan `SellerRequiredMixin`, que verifica no solo si el usuario está logueado, sino si tiene permisos de vendedor explícitos.
-   **Protección de Rutas**: Los clientes no pueden acceder a las URLs de gestión de inventario incluso si conocen la ruta.

### 3. Prevención de Inyección y Manipulación (IDOR)
-   **Tracking Seguro**: Para el rastreo de pedidos, no se exponen IDs incrementales. Se utiliza un `tracking_token` (UUID4) que es virtualmente imposible de adivinar.
-   **Validación de Precio en Backend**: El precio final de un pedido **no se recibe desde el navegador**. Se recalcula en el servidor consultando la base de datos para evitar que usuarios alteren el costo total modificando el código del frontend.

### 4. Seguridad en el Transporte y Datos
-   **Variables de Entorno**: Datos sensibles (Secret Key, Números de teléfono) están fuera del código fuente en un archivo `.env`.
-   **No-Sniffing**: Se fuerza al navegador a respetar los tipos MIME definidos por el servidor, previniendo ataques de "MIME sniffing".

## 🔎 Rationale (Por qué estas medidas)

-   **Precio en Backend**: En un negocio de personalización, el riesgo de que alguien cambie un valor `$100.00` por `$1.00` en el navegador es alto. Calcularlo en el servidor es la medida de protección de ingresos más crítica.
-   **UUID vs ID**: Exponer IDs (`/order/1/`) permite que competidores o curiosos vean el volumen de ventas o accedan a datos de otros clientes. El UUID garantiza privacidad.
-   **Sellers Mixin**: Evita el "escalamiento de privilegios", donde un cliente normal intenta actuar como administrador.
