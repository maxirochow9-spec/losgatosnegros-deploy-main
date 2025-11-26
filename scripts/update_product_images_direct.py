import os
import sys
from pathlib import Path
# Asegurar que el path del proyecto esté en sys.path para poder importar `core.settings`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from tienda.models import Producto

# Usar coincidencias por palabra clave en lugar de nombres exactos (cubrir apóstrofes y variaciones)
keywords_map = [
    (['ballent', 'ballantine', "ballantine's"], '/static/tienda/img/ballentine-promo.png'),
    (['jack'], '/static/tienda/img/jack-promo.png'),
    (['johnnie', 'johnny', 'walker'], '/static/tienda/img/jhonnie-promo.png'),
    (['sandy'], '/static/tienda/img/sandy-promo.png'),
]

def find_image_for_name(name_lower: str):
    for keys, path in keywords_map:
        for k in keys:
            if k in name_lower:
                return path
    return None

updated = 0
for p in Producto.objects.all():
    nombre = (p.nombre or '').strip()
    name_lower = nombre.lower()
    new_img = find_image_for_name(name_lower)
    if new_img:
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
