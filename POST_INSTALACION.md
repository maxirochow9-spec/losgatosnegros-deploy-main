# Guía Post-Instalación - Los Gatos Negros

## ✅ Pasos Completados

Después de ejecutar la instalación, deberías tener:

- [x] Entorno virtual creado y activado
- [x] Dependencias instaladas
- [x] Base de datos PostgreSQL migrada
- [x] Servidor ejecutándose en `http://localhost:8000`

## 🔍 Verificar Instalación

### 1. Acceder a la Aplicación

```
Página de Inicio:   http://localhost:8000/
Catálogo:           http://localhost:8000/catalogo/
Panel de Admin:      http://localhost:8000/admin/
```

### 2. Crear un Superusuario (Opcional)

Si deseas acceder al panel de administración:

```bash
python manage.py createsuperuser
```

Ingresa:
- Nombre de usuario: `admin`
- Email: `admin@example.com`
- Contraseña: (tu contraseña)

## 📝 Configuración Importante

### 1. Cambiar Número de WhatsApp

En `tienda/static/tienda/catalog.js`, línea ~175:

```javascript
// ANTES
const whatsappUrl = `https://wa.me/56912345678?text=${encodedMessage}`;

// DESPUÉS (reemplaza con tu número)
const whatsappUrl = `https://wa.me/TU_NUMERO_AQUI?text=${encodedMessage}`;
```

**Formato del número:**
- Código de país + número sin espacios
- Ej: Chile 56912345678 (sin +)

### 2. Información de Contacto

Edita los templates para actualizar:

#### En `home.html` y `catalog.html`:

```html
<!-- Footer -->
<div class="col-md-4 mb-4">
    <h5 class="footer-title">Contacto</h5>
    <a href="mailto:info@losgatosnegros.cl" class="footer-link">
        info@losgatosnegros.cl  <!-- Cambia esto -->
    </a>
    <a href="tel:+56912345678" class="footer-link">
        +56 9 1234 5678  <!-- Cambia esto -->
    </a>
    <p class="footer-link">Valdivia, Chile</p>  <!-- Cambia esto -->
</div>
```

### 3. Agregar Productos

#### Opción 1: Panel de Administración (Recomendado)

1. Accede a `http://localhost:8000/admin/`
2. Inicia sesión con tu superusuario
3. Haz clic en "Productos"
4. Haz clic en "Agregar Producto +"
5. Completa los campos:
   - **Nombre**: Nombre del producto
   - **Precio**: En pesos chilenos (ej: 5990)
   - **Imagen**: URL de la imagen
   - **Tipo**: Alcohólica o No alcohólica

#### Opción 2: Base de Datos Directa

```bash
python manage.py shell
```

```python
from tienda.models import Producto

# Crear un producto
producto = Producto(
    nombre="Vino Tinto Reserve",
    precio=8990,
    imagen="https://url-imagen.com/vino.jpg",
    tipo="alcoholic"
)
producto.save()

# Ver todos los productos
Producto.objects.all()
```

## 🎨 Personalización

### 1. Cambiar Tema de Colores

En `tienda/static/tienda/styles.css`, líneas 1-25:

```css
:root {
    /* Acentos */
    --accent: #ff9e00;              /* Color naranja principal */
    --accent-hover: #e68a00;        /* Naranja más oscuro al hover */
    
    /* Fondos */
    --dark-bg: #0f0f0f;             /* Fondo oscuro */
    --dark-card: #1a1a1a;           /* Fondo de tarjetas */
}
```

Cambia estos valores a los colores que desees.

### 2. Cambiar Textos del Sitio

**Nombre del negocio:**
```bash
# Busca y reemplaza "Los Gatos Negros" por tu nombre
# En: home.html, catalog.html, styles.css
```

**Sección de Características:**
En `home.html`, sección `<!-- Features Section -->`, personaliza:
- Títulos
- Descripciones
- Iconos

### 3. Cambiar Imágenes de Fondo

En `styles.css`, busca `.hero`:

```css
.hero {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8)), 
                url('NUEVA_URL_IMAGEN_AQUI');
}
```

## ⚙️ Configuración de Producción

### 1. Preparar para Producción

Crea un archivo `.env`:

```
SECRET_KEY=tu_nueva_secret_key_muy_larga_aleatoria
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/basedatos
```

### 2. Actualizar `settings.py`

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

### 3. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 4. Usar Gunicorn (Producc)

```bash
pip install gunicorn

gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Solucionar Problemas

### Error: "No module named 'django'"

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "database "losgatosdb" does not exist"

```bash
# Crea la base de datos en PostgreSQL
psql -U postgres

postgres=# CREATE DATABASE losgatosdb;
postgres=# \q
```

### Error: "port 5432 refused"

PostgreSQL no está ejecutándose:

```bash
# Windows (si tienes PostgreSQL instalado)
net start postgresql-x64-13

# macOS
brew services start postgresql

# Linux
sudo service postgresql start
```

### Error: "psycopg2 error"

```bash
# Reinstala psycopg2
pip install --force-reinstall psycopg2-binary
```

## 📊 Estructura de Base de Datos

### Tabla `tienda_producto`

```
id (AutoField)          - Identificador único
nombre (CharField)      - Nombre del producto (máx 100 caracteres)
precio (DecimalField)   - Precio en pesos
imagen (URLField)       - URL de la imagen del producto
tipo (CharField)        - Tipo: "alcoholic" o "non-alcoholic"
created_at (DateTime)   - Fecha de creación (automática)
updated_at (DateTime)   - Fecha de actualización (automática)
```

## 🔐 Seguridad

1. **Nunca compartas tu `SECRET_KEY`**
2. **No subas `.env` a control de versiones**
3. **Usa HTTPS en producción**
4. **Actualiza Django regularmente**
5. **Valida siempre los datos del usuario**

## 📱 Pruebas en Dispositivos

### Prueba Responsiva en Desktop

```
http://localhost:8000 → Abre DevTools (F12)
Cambia a modo dispositivo (Ctrl+Shift+M)
Prueba en diferentes resoluciones
```

### Prueba en Móvil Real

```bash
# En lugar de localhost, usa tu IP local
# En el terminal donde ejecutas el servidor:
python manage.py runserver 0.0.0.0:8000

# En tu móvil (conectado a la misma WiFi):
http://TU_IP_LOCAL:8000
# Ej: http://192.168.1.100:8000
```

## 📚 Recursos Útiles

- [Documentación Django](https://docs.djangoproject.com/)
- [Documentación PostgreSQL](https://www.postgresql.org/docs/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

## ✨ Siguientes Pasos

1. ✅ Personalizar información del sitio
2. ✅ Agregar productos a la base de datos
3. ✅ Probar en dispositivos móviles
4. ✅ Configurar dominio y hosting
5. ✅ Preparar para producción

## 📞 Soporte

Si encuentras problemas:

1. Verifica que PostgreSQL esté ejecutándose
2. Verifica que el entorno virtual esté activado
3. Lee los mensajes de error cuidadosamente
4. Consulta la documentación oficial

---

**¡Tu aplicación está lista para usar!** 🎉

Versión: 2.0 | Fecha: 13 de noviembre de 2025
