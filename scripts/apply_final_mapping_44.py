import os
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from tienda.models import Producto

pid = 44
fname = 'blackvodka-promo.png'
try:
    p = Producto.objects.get(id=pid)
except Producto.DoesNotExist:
    print(f"Producto id={pid} no existe")
    sys.exit(1)
new_img = f"/static/tienda/img/{fname}"
if p.imagen != new_img:
    p.imagen = new_img
    p.save()
    print(f"Aplicado: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
else:
    print(f"Sin cambios: id={p.id} ya tiene imagen='{p.imagen}'")
