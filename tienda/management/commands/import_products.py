import os
import json
from decimal import Decimal

from django.core.management.base import BaseCommand

from tienda.models import Producto


class Command(BaseCommand):
    help = 'Import products from a JSON file into tienda.Producto (fixture or plain list)'

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', default='tienda/fixtures/products.json', help='Path to JSON file')
        parser.add_argument('--flush', action='store_true', help='Delete existing products before import')
        parser.add_argument('--update', action='store_true', help='Update existing products matched by nombre')

    def handle(self, *args, **options):
        path = options['file']
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f'File not found: {path}'))
            return

        with open(path, 'r', encoding='utf-8') as fh:
            try:
                data = json.load(fh)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error parsing JSON: {e}'))
                return

        # Support Django fixture format (list of {model, pk, fields}) or plain list of objects
        items = []
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and 'fields' in data[0]:
            for obj in data:
                fields = obj.get('fields', {})
                items.append(fields)
        elif isinstance(data, list):
            items = data
        else:
            self.stderr.write(self.style.ERROR('Unsupported JSON structure: expected a list'))
            return

        if options['flush']:
            Producto.objects.all().delete()
            self.stdout.write(self.style.WARNING('Deleted existing products.'))

        created = 0
        updated = 0
        skipped = 0

        for item in items:
            nombre = item.get('nombre') or item.get('name')
            if not nombre:
                self.stderr.write(self.style.WARNING(f'Skipping item without nombre: {item}'))
                continue

            precio_raw = item.get('precio') or item.get('price') or '0'
            try:
                precio = Decimal(str(precio_raw))
            except Exception:
                precio = Decimal('0')

            imagen = item.get('imagen') or item.get('image') or ''
            tipo = item.get('tipo') or item.get('type') or 'non-alcoholic'

            try:
                existing = Producto.objects.filter(nombre=nombre).first()
                if existing:
                    if options['update']:
                        existing.precio = precio
                        existing.imagen = imagen
                        existing.tipo = tipo
                        existing.save()
                        updated += 1
                        self.stdout.write(f'Updated: {nombre}')
                    else:
                        skipped += 1
                        self.stdout.write(f'Skipped (exists): {nombre}')
                else:
                    Producto.objects.create(nombre=nombre, precio=precio, imagen=imagen, tipo=tipo)
                    created += 1
                    self.stdout.write(f'Created: {nombre}')
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error saving {nombre}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Import finished. Created={created} Updated={updated} Skipped={skipped}'))
