import os
import sys
import re
from pathlib import Path

# Preparar entorno Django
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from tienda.models import Producto

IMG_DIR = PROJECT_ROOT / 'static' / 'tienda' / 'img'
if not IMG_DIR.exists():
    print('No se encontró el directorio de imágenes:', IMG_DIR)
    sys.exit(1)

# Normalizar texto: quitar acentos, puntuación y convertir a minúsculas
import unicodedata

def normalize(s):
    s = (s or '')
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", ' ', s)
    return s.strip()

# Lista de archivos de imagen disponibles
files = [f for f in os.listdir(IMG_DIR) if os.path.isfile(IMG_DIR / f)]
files_norm = {f: normalize(f) for f in files}

# Productos que no tienen imagen local (no empiezan con /static/tienda/img/)
products = list(Producto.objects.all().order_by('id'))
no_local = [p for p in products if not (p.imagen or '').startswith('/static/tienda/img/')]

print('Archivos de imagen disponibles:')
for f in files:
    print(' -', f)
print('\nProductos sin imagen local (se intentará mapear):')
for p in no_local:
    print(f' - id={p.id} nombre="{p.nombre}"')

# Intentar mapear: buscaremos si alguno de los tokens del nombre aparece en el nombre de archivo
proposals = {}
for p in no_local:
    norm_name = normalize(p.nombre)
    tokens = [t for t in norm_name.split() if len(t) >= 3]
    matches = []
    for fname, fnorm in files_norm.items():
        for t in tokens:
            if t in fnorm:
                matches.append(fname)
                break
    # dedupe
    matches = list(dict.fromkeys(matches))
    proposals[p.id] = matches

# Mostrar propuestas
print('\nPropuestas de mapeo (producto id -> [archivos coincidentes]):')
for pid, matches in proposals.items():
    print(pid, '->', matches)

# Aplicar solo mapeos unívocos
applied = 0
for p in no_local:
    matches = proposals.get(p.id, [])
    if len(matches) == 1:
        new_img = f"/static/tienda/img/{matches[0]}"
        if p.imagen != new_img:
            p.imagen = new_img
            p.save()
            print(f"Aplicado: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
            applied += 1
    else:
        if len(matches) == 0:
            print(f"No matches para id={p.id} nombre='{p.nombre}'")
        else:
            print(f"Multiples matches para id={p.id} nombre='{p.nombre}': {matches}")

print(f"\nTotal aplicados automát. unívocos: {applied}")
print('Si quieres que aplique alguno de los mapeos múltiples, indícamelo (formato: id:filename).')
