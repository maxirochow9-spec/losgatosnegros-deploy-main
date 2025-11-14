# Los Gatos Negros - Delivery de Bebidas

Sistema de delivery de bebidas en línea desarrollado con Django, HTML, CSS y JavaScript. La plataforma permite a los usuarios explorar un catálogo de bebidas alcohólicas y no alcohólicas, agregar productos al carrito y realizar pedidos a través de WhatsApp.

## 🚀 Características

- **Separación de páginas**: Página de inicio atractiva y catálogo dedicado
- **Base de datos PostgreSQL**: Migración de MySQL a PostgreSQL para mejor rendimiento
- **Carrito de compras**: Sistema funcional con almacenamiento en localStorage
- **Filtrado de productos**: Búsqueda y filtrado por tipo de bebida
- **Animaciones mejoradas**: Efectos visuales modernos en toda la aplicación
- **Diseño responsivo**: Optimizado para dispositivos móviles y desktop
- **Integración WhatsApp**: Envío de pedidos directamente por WhatsApp
- **Autenticación básica**: Sistema de login y registro

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd losgatosnegros
```

### 2. Crear entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE losgatosdb;
```

**Nota**: Asegúrate de que PostgreSQL esté ejecutándose en `localhost:5432` con usuario `postgres` y contraseña `postgres`. Si deseas cambiar estas credenciales, edita `core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'losgatosdb',
        'USER': 'tu_usuario',        # Cambiar aquí
        'PASSWORD': 'tu_contraseña', # Cambiar aquí
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear un usuario administrador.

### 7. Cargar datos iniciales (opcional)

Puedes agregar productos desde el panel de administración:

```bash
python manage.py runserver
```

Luego accede a `http://localhost:8000/admin/` con tus credenciales de superusuario.

## 🏃 Ejecutar la aplicación

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000/`

## 📱 Páginas principales

- **Inicio (`/`)**: Página de bienvenida con información sobre el servicio, características y categorías
- **Catálogo (`/catalogo/`)**: Listado completo de productos con filtros de búsqueda
- **Administración (`/admin/`)**: Panel de control para gestionar productos

## 📂 Estructura del Proyecto

```
losgatosnegros/
├── manage.py                          # Utilidad de línea de comandos de Django
├── requirements.txt                   # Dependencias del proyecto
├── README.md                          # Este archivo
│
├── core/                              # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py                   # Configuración de Django (DB, apps, etc)
│   ├── urls.py                       # Rutas principales del proyecto
│   ├── wsgi.py                       # WSGI de producción
│   └── asgi.py                       # ASGI de producción
│
└── tienda/                            # Aplicación principal
    ├── migrations/                    # Migraciones de base de datos
    ├── static/
    │   └── tienda/
    │       ├── styles.css            # Estilos mejorados con animaciones
    │       ├── main.js               # JavaScript (legado)
    │       ├── home.js               # JavaScript para página de inicio
    │       └── catalog.js            # JavaScript para catálogo
    ├── templates/
    │   └── tienda/
    │       ├── home.html             # Página de inicio
    │       └── catalog.html          # Página del catálogo
    ├── __init__.py
    ├── admin.py                       # Configuración de panel admin
    ├── apps.py
    ├── models.py                      # Modelos de datos
    ├── tests.py
    └── views.py                       # Vistas de la aplicación
```

## 🎨 Mejoras Implementadas

### UI/UX
- **Página de inicio mejorada**: Con animaciones de partículas, información sobre el servicio y estadísticas
- **Animaciones suaves**: Transiciones elegantes en botones, tarjetas y elementos
- **Gradientes modernos**: Fondos dinámicos que mejoran la experiencia visual
- **Diseño responsivo**: Optimizado para todos los tamaños de pantalla

### Backend
- **Migración a PostgreSQL**: Base de datos más robusta y escalable
- **Vistas separadas**: Lógica de negocio organizada en `home()` y `catalog()`
- **Filtrado de productos**: Búsqueda por tipo desde URL y formularios

### Frontend
- **Carga perezosa**: Imágenes con `lazy loading` para mejor rendimiento
- **Efectos visuales**: Botones con ripple effect y tarjetas con hover effects
- **Sistema de notificaciones**: Toast notifications para feedback al usuario

## 🛠️ Configuración Adicional

### Cambiar número de WhatsApp

En `tienda/static/tienda/catalog.js`, busca esta línea:

```javascript
const whatsappUrl = `https://wa.me/56912345678?text=${encodedMessage}`;
```

Reemplaza `56912345678` con tu número de WhatsApp (formato: código país + número sin espacios).

### Personalizar información del sitio

- **Nombre del negocio**: En cualquier template, edita "Los Gatos Negros"
- **Dirección, teléfono, emails**: En el footer (dentro de los templates HTML)
- **Horarios**: En la sección de footer

## 🔐 Consideraciones de Seguridad

Para producción:

1. **Cambiar `SECRET_KEY`** en `core/settings.py`
2. **Establecer `DEBUG = False`** en producción
3. **Configurar `ALLOWED_HOSTS`** con tu dominio
4. **Usar variables de entorno** para credenciales:

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## 📦 Tecnologías Utilizadas

- **Backend**: Django 5.2.8
- **Base de datos**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Framework CSS**: Bootstrap 5.3
- **Iconos**: Bootstrap Icons
- **Almacenamiento cliente**: LocalStorage

## 🤝 Contribución

Este proyecto es educativo y está abierto a mejoras. Siéntete libre de:

- Reportar problemas
- Sugerir nuevas características
- Mejorar el código

## 📞 Soporte

Para preguntas o problemas, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

---

**Última actualización**: 13 de noviembre de 2025

**Versión**: 2.0 (PostgreSQL + UI mejorada)
