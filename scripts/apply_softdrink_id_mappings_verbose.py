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
    58: 'becker-12.png',
    59: 'cocacola.png',
    60: 'fanta.png',
    61: 'sprite.png',
    62: 'kemxtreme.png',
}

static_dir = PROJECT_ROOT / 'static' / 'tienda' / 'img'

applied = 0

for pid, fname in mappings.items():
    print('---')
    print(f'Procesando id={pid} -> {fname}')
    try:
        p = Producto.objects.get(id=pid)
    except Producto.DoesNotExist:
        print(f'ERROR: Producto id={pid} no existe en la base de datos')
        continue
    print(f'Antes: id={p.id} nombre="{p.nombre}" imagen="{p.imagen}"')

    file_path = static_dir / fname
    if not file_path.exists():
        print(f'ERROR: El archivo {file_path} no existe en el repo. Revisa `static/tienda/img/`')
        continue

    new_img = f'/static/tienda/img/{fname}'
    if p.imagen == new_img:
        print('No se aplicó: ya tiene la misma ruta de imagen')
        continue

    # Aplicar cambio
    p.imagen = new_img
    p.save()
    applied += 1
    print(f'Después: id={p.id} nombre="{p.nombre}" imagen="{p.imagen}" (guardado)')

print('---')
print(f'Total aplicados: {applied}')
