from rest_framework import serializers

# TODO: Ajusta el import del modelo Product a tu app y nombre real.
# Ejemplo: from shop.models import Product
# Si no sabes el nombre de la app, reemplaza el import por el siguiente patrón:
# from django.apps import apps
# Product = apps.get_model('your_app_name', 'Product')

from tienda.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Ajusta los campos según tu modelo real
        fields = ['id', 'name', 'slug', 'price', 'image_url', 'category', 'available']
