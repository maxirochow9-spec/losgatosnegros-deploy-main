import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from tienda.models import Producto

# Mapear por palabra clave en el nombre del producto -> filename en static
keyword_mappings = {
    'coca': 'cocacola.png',
    'sprite': 'sprite.png',
    'fanta': 'fanta.png',
    'kem': 'kemxtreme.png',
}

applied_total = 0
not_found = []

for keyword, fname in keyword_mappings.items():
    qs = Producto.objects.filter(nombre__icontains=keyword)
    if not qs.exists():
        not_found.append(keyword)
        print(f"No se encontraron productos con '{keyword}' en el nombre")
        continue
    for p in qs:
        new_img = f"/static/tienda/img/{fname}"
        if p.imagen != new_img:
            p.imagen = new_img
            p.save()
            applied_total += 1
            print(f"Aplicado: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
        else:
            print(f"Sin cambios: id={p.id} nombre='{p.nombre}' ya tiene imagen='{p.imagen}'")

print(f"Total de asignaciones aplicadas: {applied_total}")
if not_found:
    print("Keywords sin matches:", ", ".join(not_found))
