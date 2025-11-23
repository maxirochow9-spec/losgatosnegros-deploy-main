from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from tienda.models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoint read-only para listar y ver detalle de productos."""
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
