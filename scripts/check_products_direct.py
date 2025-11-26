import os
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from tienda.models import Producto

for p in Producto.objects.all().order_by('id'):
    print(f"id={p.id}\tnombre='{p.nombre}'\timagen='{p.imagen}'")
print('Total:', Producto.objects.count())
