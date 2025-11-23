from django.contrib import admin
from django.apps import apps

Product = None
try:
    Product = apps.get_model('tienda', 'Product')
except Exception:
    Product = None

if Product is not None:
    try:
        admin.site.register(Product)
    except Exception:
        # If already registered or registration fails, ignore here — the target project will control admin.
        pass
