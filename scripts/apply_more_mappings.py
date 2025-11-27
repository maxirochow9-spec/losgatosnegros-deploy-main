import os
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from tienda.models import Producto

mappings = {
    46: 'blancovodka-promo.png',
    47: 'ron-promo.png',
    51: 'vinos.png',
}

applied = 0
for pid, fname in mappings.items():
    try:
        p = Producto.objects.get(id=pid)
    except Producto.DoesNotExist:
        print(f"Producto id={pid} no existe")
        continue
    new_img = f"/static/tienda/img/{fname}"
    if p.imagen != new_img:
        p.imagen = new_img
        p.save()
        print(f"Aplicado: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
        applied += 1
    else:
        print(f"Sin cambios: id={p.id} ya tiene imagen='{p.imagen}'")

print(f"Total aplicados: {applied}")
