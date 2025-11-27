**Proyecto Los Gatos Negros**

- **Descripción:**: Sitio de e-commerce pequeño construido con Django. Permite listar productos (bebidas, cervezas, etc.), agregar al carrito y realizar pedidos que se pueden enviar por WhatsApp. El proyecto está preparado para deploy en plataformas tipo Render y sirve archivos estáticos con WhiteNoise.

**Estado Actual**
- **Stack:**: Django 5.2.x, Python 3.x, WhiteNoise, Gunicorn, PostgreSQL (conexión por `DATABASE_URL` o variables de entorno), Bootstrap en frontend.
- **Objetivo:**: desplegar en Render con `collectstatic` y servir estáticos; tener catálogo con filtrado y búsqueda; disponer de scripts para mapear imágenes locales a productos en la base de datos.

**Estructura del repositorio (resumen)**
- **`core/`**: configuración del proyecto Django (contiene `settings.py`, `wsgi.py`, `asgi.py`, `urls.py`).
- **`tienda/`**: app principal con modelos, vistas, templates y archivos estáticos.
  - **`tienda/models.py`**: definición de `Producto` y otros modelos.
  - **`tienda/views.py`**: vistas de catálogo, home y checkout (incluye manejo temporal de errores de BD).
  - **`tienda/templates/tienda/`**: plantillas `home.html`, `catalog.html`, `index.html`.
  - **`tienda/static/tienda/`**: JS/CSS y `img/` con imágenes usadas en el catálogo (`styles.css`, `catalog.js`, `main.js`, `home.js`, `img/*.png`).
- **`static/` y `staticfiles/`**: directorios usados localmente y para `collectstatic`.
- **`scripts/`**: utilidades para mapear/actualizar `Producto.imagen` en la base de datos desde archivos locales.

**Qué hace el proyecto (funcionalidades clave)**
- **Catálogo**: lista de productos, con filtrado por tipo y búsqueda. Se añadió filtrado cliente-side con búsqueda "fuzzy" (token/subsequence), debounce y sincronización de parámetros (`q`, `type`) en la URL.
- **Carrito y Checkout**: carrito guardado en `localStorage`, modal de checkout que persiste pedidos en el servidor y redirige a WhatsApp con el pedido formateado.
- **Asignación de imágenes**: varios scripts en `scripts/` para automatizar el mapeo entre archivos en `static/tienda/img/` y los registros de `Producto` (incluyen comprobaciones para existencia de archivos y mapeos manuales por ID).

**Instalación y desarrollo local**
- **Requisitos:**: Python 3.10+ (ajustar según su entorno), Git.
- **Pasos rápidos (Windows PowerShell)**:

```powershell
# Crear y activar entorno virtual (ajusta si ya tienes otro)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# (Opcional) cargar datos de ejemplo o mapear imágenes usando scripts en `scripts/`

# Ejecutar servidor de desarrollo
python manage.py runserver
```

- **Collectstatic (local/prod):**
```powershell
python manage.py collectstatic --noinput
```

**Variables de entorno importantes**
- **`SECRET_KEY`**: clave secreta de Django. En producción debe estar en variables del entorno.
- **`DEBUG`**: `True`/`False`. En producción `False`.
- **`DATABASE_URL`** o configuración `POSTGRES_*`: cadena de conexión a la base de datos PostgreSQL.
- **`ALLOWED_HOSTS`**: incluye host de Render o `RENDER_EXTERNAL_HOSTNAME`.
- **`RENDER_EXTERNAL_HOSTNAME`**: variable que Render expone (usada para `ALLOWED_HOSTS`).

**Deploy en Render (notas prácticas)**
- **Build command recomendado:**: usar un script `build.sh` que instale dependencias, migre y ejecute `collectstatic`. Ejemplo simplificado en Render:

```
bash build.sh
```

- **Start command:**: servidor WSGI, p. ej. `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`.
- **Archivos a configurar en dashboard de Render:**: variables de entorno (`SECRET_KEY`, `DATABASE_URL`, `DEBUG=false`, `ALLOWED_HOSTS`, `RENDER_EXTERNAL_HOSTNAME`), planificar que `collectstatic` corra en build.
- **WhiteNoise:**: configurado en `core/settings.py` para servir estáticos en producción sin necesidad de un servidor de archivos separado.

**Scripts / utilidades importantes (`scripts/`)**
- **`apply_softdrink_mappings.py`**: intenta mapear productos con nombres que contengan palabras clave (coca, sprite, fanta, kem, etc.) a imágenes correspondientes.
- **`apply_softdrink_id_mappings.py`** y variantes `*_verbose.py`: mapeos por ID (útiles cuando se conocen los IDs exactos a actualizar); las variantes `verbose` imprimen mensajes y verifican existencia del archivo antes de guardar.
- **`check_products.py`**: lista `id, nombre, imagen` de cada `Producto` para verificación manual.
- **Uso:** ejecutar con el entorno virtual activado y las variables de conexión a la BD configuradas; los scripts usan el ORM de Django (pueden requerir `DJANGO_SETTINGS_MODULE` si se ejecutan fuera del `manage.py`).

**Frontend: detalles**
- **`tienda/static/tienda/catalog.js`**: lógica de renderizado del catálogo en cliente, construcción del array `products` desde el DOM cuando el HTML es renderizado por Django, ahora con búsqueda fuzzy y debounce.
- **`tienda/templates/tienda/catalog.html`**: markup del catálogo. El JS puede trabajar tanto con HTML renderizado por el servidor como con datos inyectados en una variable JS `products`.
- **WhatsApp:** número configurado en plantillas y JS (`56966344411`). La redirección a `https://wa.me/` se usa con el texto del pedido codificado.

**Problemas conocidos y recomendaciones**
- **Errores `OperationalError` al iniciar en producción**: pueden deberse a problemas de red/IPv6 con la base de datos (observado en despliegues). Recomendaciones:
  - Verificar que la DB permita conexiones desde Render y que la cadena `DATABASE_URL` sea correcta.
  - Forzar conexión IPv4 si el proveedor lo requiere o ajustar opciones de red.
- **Tamaño del repositorio por imágenes**: actualmente hay muchas imágenes en `static/tienda/img/`. Para producción se recomienda mover a un almacenamiento de objetos (S3, DigitalOcean Spaces, Supabase Storage) y almacenar URLs públicas en `Producto.imagen`.
- **Observabilidad:** añadir Sentry para errores en producción y monitoreo de la base de datos.

**Mejoras sugeridas (roadmap corto)**
- Migrar imágenes estáticas a almacenamiento de objetos y actualizar scripts para escribir URLs públicas.
- Implementar endpoint API paginado para búsqueda remota (útil si el catálogo crece) y reemplazar parte del filtrado cliente por consultas paginadas.
- Añadir tests unitarios para vistas críticas y scripts de mapeo.

**Cómo contribuir / flujo de trabajo**
- **Fork / Branch:** crear ramas por feature/bugfix y abrir PR a `main`.
- **Commit messages:** claros y concisos. Ejemplo actual: `Catalog: client-side fuzzy search, debounce and URL param sync`.

**Archivos útiles para revisar**
- `core/settings.py` — configuración de WhiteNoise, `STATIC_ROOT` y variables de entorno.
- `tienda/views.py` — vistas de catálogo, home y manejo de errores.
- `tienda/static/tienda/catalog.js` — nueva lógica de búsqueda y filtrado cliente-side.
- `scripts/` — scripts de mapeo de imágenes a `Producto`.

**Contacto / Autor**
- Repositorio: `https://github.com/maxirochow9-spec/losgatosnegros-deploy-main`
- Para dudas o tareas adicionales: abrir un issue o enviar un PR.

---

Si quieres, puedo:
- Commitear este `README.md` y pushearlo por ti.
- Añadir una versión en inglés.
- Generar un `README` más conciso para la página principal del repo con badges (build, python, license).

Indica si quieres que haga el commit ahora o que haga cambios en el contenido del README.
