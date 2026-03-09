# Manual de Usuario e Instalación — Sisart

Este documento detalla los pasos para poner en marcha el sistema de gestión de floristería Sisart en un entorno de desarrollo.

## 🛠️ Requisitos Previos

-   **Python 3.12** o superior.
-   **Git** (opcional, para clonar el repositorio).
-   **Virtualenv** para gestión de entornos.

## 🚀 Instalación Paso a Paso

1.  **Clonar o Descargar el Proyecto**:
    ```bash
    git clone https://github.com/usuario/SistemaFlores.git
    cd SistemaFlores
    ```

2.  **Crear y Activar Entorno Virtual**:
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en la raíz con el siguiente contenido base:
    ```env
    DEBUG=True
    SECRET_KEY=tu_clave_secreta_aqui
    WHATSAPP_NUMBER=573000000000
    ```

5.  **Ejecutar Migraciones**:
    ```bash
    python manage.py migrate
    ```

6.  **Crear Superusuario (Vendedor)**:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Iniciar el Servidor**:
    ```bash
    python manage.py runserver
    ```

## 📝 Uso Inicial

-   **Acceso Vendedor**: Entra a `http://127.0.0.1:8000/admin/` o loguéate en la web con la cuenta superusuario para acceder al Dashboard administrativo.
-   **Carga de Datos**: Es recomendable empezar cargando **Flores** y **Tamaños de Ramos** en el catálogo para habilitar el diseñador.
-   **Acceso Cliente**: Cualquier usuario que se registre a través del formulario "Registrarse" tendrá el rol de cliente automáticamente.
