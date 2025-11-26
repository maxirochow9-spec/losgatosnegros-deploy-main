import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from tienda.models import Producto

KEEP_IDS = {37, 38, 39, 40}  # Los 4 productos que sí deben tener imagenes locales
TARGET = '/static/tienda/img/sandy-promo.png'

reverted = 0
for p in Producto.objects.filter(imagen=TARGET):
    if p.id in KEEP_IDS:
        print(f"Mantener imagen para id={p.id} nombre='{p.nombre}'")
        continue
    # generar placeholder con el nombre del producto
    text = p.nombre or 'Producto'
    # limitar longitud para evitar urls demasiado largas
    text_short = text[:60]
    placeholder = f"https://via.placeholder.com/400x300.png?text={quote_plus(text_short)}"
    p.imagen = placeholder
    p.save()
    print(f"Revertido: id={p.id} nombre='{p.nombre}' -> imagen='{p.imagen}'")
    reverted += 1

print(f"Total revertidos: {reverted}")
