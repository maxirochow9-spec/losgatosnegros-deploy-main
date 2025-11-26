jugo-naranja# Este script será pasado a `python manage.py shell < scripts/update_product_images.py`
from tienda.models import Producto

# Mapea nombres de producto a rutas estáticas locales
mapping = {
    'Cerveza Negra': '/static/tienda/img/ballentine-promo.png',
    'Cider Natural': '/static/tienda/img/jack-promo.png',
    'Jugo Tropical': '/static/tienda/img/sandy-promo.png',
    'Gaseosa Cola': '/static/tienda/img/jhonnie-promo.png',
    'Vino Tinto': '/static/tienda/img/ballentine-promo.png',
}

updated = 0
for p in Producto.objects.all():
    nombre = (p.nombre or '').strip()
    if nombre in mapping:
        new_img = mapping[nombre]
        if p.imagen != new_img:
            p.imagen = new_img
            p.save()
            print(f"Actualizado: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
            updated += 1
        else:
            print(f"Sin cambios: id={p.id} nombre='{p.nombre}' ya tiene imagen='{p.imagen}'")
    else:
        print(f"Sin mapeo para: id={p.id} nombre='{p.nombre}' (no se actualizó)")

print(f"Total actualizados: {updated}")
