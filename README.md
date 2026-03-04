# 💐 Atelier Floral – Sistema de Gestión de Ramos Personalizados

Este proyecto es un sistema integral basado en Django para la creación, personalización y venta de ramos de flores artesanales. Combina un constructor visual premium en el frontend con una robusta lógica de negocio en el backend.

## 🏗️ Arquitectura del Sistema (Backend - Django)

El sistema está organizado en aplicaciones modulares para facilitar el mantenimiento e integración de nuevas funcionalidades:

### 1. `apps.accounts` (Usuarios y Roles)
- Gestiona los perfiles de **Vendedor** y **Cliente**.
- Define permisos y accesos diferenciados.

### 2. `apps.catalog` (Gestión de Inventario)
- **Flores**: Almacena catálogo de flores con precios y tallas (L, M, S).
- **BouquetSizes**: Define los límites de composición (cuántas flores caben según el tamaño del ramo).

### 3. `apps.bouquet` (Taller de Diseño)
- **Bouquet**: Instancia de un diseño específico.
- **BouquetItem**: Guarda la "receta" visual personalizada (coordenadas x/y, escala, rotación y flor específica).

### 4. `apps.orders` (Transacciones)
- Gestiona el **Pedido** final.
- Integra el subsistema de **Cupones de Descuento** (`apps.discounts`).
- Calcula totales, estados de envío y genera mensajes para ventas vía WhatsApp.

### 5. `apps.dahsboard` (Interfaz de Gestión)
- Provee el **Menú Dinámico** que se adapta según el rol del usuario conectado.

---

## 🎨 El Constructor Visual (Frontend)

Ubicado en `apps/bouquet/templates/bouquet/designer.html` y apoyado por `static/js/script.js`.

### Características Inteligentes:
- **Restricción de Capas**: Las flores pequeñas no pueden superar la altura de las medianas, manteniendo la estética natural.
- **Jerarquía de Escala**: Escalamiento lógico basado en la profundidad de la capa (Fondo > Cuerpo > Frente).
- **Herramientas de Edición**: Dial de rotación intuitivo, sliders de escala y opción de arrastrar y soltar (Drag & Drop).
- **Integración Backend**: Los datos de flores se inyectan dinámicamente desde la base de datos de Django para asegurar precios consistentes.

---

## 🔄 El Flujo de Trabajo

1. **Selección**: El cliente elige un tamaño de ramo (que define presupuesto y límites).
2. **Diseño**: El usuario arma su ramo usando el constructor visual.
3. **Validación**: Al finalizar, Django valida que la composición cumpla con los límites de flores permitidos.
4. **Almacenamiento**: Se guarda el pedido en la base de datos vinculándolo al usuario o sesión.
5. **Cierre**: El sistema genera un mensaje de WhatsApp con el resumen del diseño y el número de pedido para finalizar la compra directamente con la florería.

---

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.12+ / Django 6.0+
- **Frontend**: Vanilla HTML5, CSS3 Premium (Flexbox/Grid), JS Moderno (ES6+).
- **Base de Datos**: SQLite3 (Desarrollo).
- **Estilos**: Estética "Atelier" con Glassmorphism y tipografía Cinzel/Cormorant.

---

## 🚀 Próximos Pasos

- **Panel de Vendedor**: Lista interactiva para que la florería vea los pedidos y previsualice los diseños 3D/2D del cliente.
- **Historial de Cliente**: Sección de "Mis Diseños" para repetir compras.
- **Dashboard de Inventario**: Interfaz para que el administrador actualice el catálogo de flores estacionales.
