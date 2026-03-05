🎯 ¿Qué estás construyendo realmente?

Un sistema de floristería con:

Constructor dinámico de ramos

Pedidos para invitados y usuarios registrados

Panel de vendedor

Menú dinámico según rol

Seguimiento de pedido con token seguro

Control de permisos por módulo

👥 ROLES DEL SISTEMA

Tienes 3 tipos principales:

Cliente invitado

Cliente registrado

Vendedor (admin interno)

🧭 MENÚ DINÁMICO SEGÚN USUARIO

Esto es clave en tu arquitectura.

En Django puedes controlar esto por:

permisos

grupos

roles personalizados

🟢 1️⃣ Cliente Invitado

No tiene cuenta.

Puede ver:

Inicio
Catálogo
Constructor de Ramos
Seguimiento de Pedido

NO puede ver:

Mi Perfil
Mis Pedidos
Dashboard

Cuando hace pedido:

Se guarda con guest_name

Se genera tracking_token

Puede hacer seguimiento con token

🔵 2️⃣ Cliente Registrado

Puede ver:

Inicio
Catálogo
Constructor
Mis Pedidos
Perfil
Cerrar sesión

Ventaja:

No necesita token manual

Puede ver historial

Puede repetir pedidos

🔴 3️⃣ Vendedor

Ve:

Dashboard
Pedidos
Clientes
Catálogo
Descuentos
Cerrar sesión

Aquí es donde entra tu manejo por módulos.

🧱 ESTRUCTURA MODULAR QUE YA DEFINIMOS

Apps:

users/
catalog/
bouquet_builder/
orders/
dashboard/
promotions/

Cada app tiene sus propios permisos.

Ejemplo en orders:

can_view_orders
can_change_order_status

Y el vendedor pertenece al grupo:

Vendedor
🔐 Seguridad que ya implementamos mentalmente

✔ CSRF protegido automáticamente por Django
✔ IDOR prevenido con tracking_token UUID
✔ No se confía en precios del frontend
✔ Validación en backend
✔ WhatsApp solo como canal informativo

🌸 Flujo real del sistema
Cliente (registrado o invitado)

Diseña ramo

Frontend envía solo IDs

Backend valida reglas

Backend calcula precio

Se crea Order

Se genera tracking_token

Opcional: abre WhatsApp

🧠 Diferencia real entre invitado y WhatsApp

Esto lo aclaramos:

Invitado = pedido en tu base de datos

WhatsApp = canal de comunicación

NO son lo mismo.

WhatsApp no reemplaza el sistema.

📊 Cómo se ve desde el vendedor

En el panel:

Pedido #A72XQ
Cliente: Invitado (Ana López)
Estado: Pending
Total: $35
Flores:
 - Rosa roja x4
 - Tulipán blanco x3

Puede cambiar estado:

Pending → Confirmed → Preparing → Ready → Delivered


recuerda pprecios dianmicos que