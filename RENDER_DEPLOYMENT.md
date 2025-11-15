# Guía de Despliegue en Render

## Configuración realizada

✅ **settings.py** - Actualizado para usar variables de entorno
✅ **requirements.txt** - Añadidas dependencias para producción (gunicorn, whitenoise)
✅ **.env** - Configurado con credenciales de Supabase
✅ **build.sh** - Script de construcción para Render
✅ **render.yaml** - Configuración de Render
✅ **Procfile** - Para ejecución en producción

## Pasos para desplegar en Render

### 1. Preparar el repositorio Git

```bash
git add .
git commit -m "Configuración para Render deployment"
git push origin main
```

### 2. Crear proyecto en Render

1. Ve a [render.com](https://render.com)
2. Inicia sesión o crea una cuenta
3. Haz clic en "New +" → "Web Service"
4. Conecta tu repositorio de GitHub
5. Selecciona el repositorio `losgatosnegros-deploy-main`

### 3. Configurar el servicio web

- **Name**: losgatosnegros
- **Environment**: Python 3
- **Build Command**: `bash build.sh`
- **Start Command**: Deja el campo vacío para que Render use el `Procfile`. El `Procfile` ya contiene:
	```
	web: gunicorn core.wsgi:application
	```
- **Plan**: Free (o el que prefieras)

### 4. Configurar variables de entorno

En Render, ve a "Environment" y añade las siguientes variables (o usa las que ya tengas configuradas):

```
SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.render.com
losgatosdb_POSTGRES_DATABASE=postgres
losgatosdb_POSTGRES_USER=postgres.duldrmfptypuvkuxpxyh
losgatosdb_POSTGRES_PASSWORD=y6AVuJ1dnZYfFBqP
losgatosdb_POSTGRES_HOST=db.duldrmfptypuvkuxpxyh.supabase.co
losgatosdb_POSTGRES_PORT=5432
NEXT_PUBLIC_SUPABASE_ANON_KEY=<tu-anon-key>
losgatosdb_SUPABASE_JWT_SECRET=<tu-jwt-secret>
losgatosdb_SUPABASE_SERVICE_ROLE_KEY=<tu-service-role-key>
losgatosdb_SUPABASE_URL=https://duldrmfptypuvkuxpxyh.supabase.co
NEXT_PUBLIC_SUPABASE_URL=https://duldrmfptypuvkuxpxyh.supabase.co
```

### 5. Generar SECRET_KEY seguro

Ejecuta esto localmente:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo en la variable `SECRET_KEY` en Render.

### 6. Desplegar

- Haz clic en "Create Web Service"
- Render ejecutará automáticamente el `build.sh` script
- Las migraciones se ejecutarán automáticamente
- Los archivos estáticos se compilarán con WhiteNoise

## Verificación post-despliegue

1. Verifica que la app esté running en `https://losgatosnegros.render.com`
2. Revisa los logs en Render para errores
3. Accede a `/admin` para verificar que Django funciona
4. Comprueba que los archivos estáticos se carguen correctamente

## Troubleshooting

### Error de conexión a base de datos
- Verifica que las credenciales de Supabase sean correctas
- Asegúrate de que Supabase permite conexiones desde Render
- Revisa los logs en Render

### Error de archivos estáticos
- Verifica que WhiteNoise esté en MIDDLEWARE
- Ejecuta `python manage.py collectstatic` localmente para probar

### Error en migraciones
- Revisa `build.sh` está siendo ejecutado
- Comprueba que las migraciones existan en Git

## Monitoreo continuo

- Render reinicia automáticamente si la app se cae
- Los logs están disponibles en el dashboard de Render
- Configura notificaciones en caso de problemas

## Actualizar después del despliegue

Para hacer cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

Render automáticamente desplegará los cambios.
