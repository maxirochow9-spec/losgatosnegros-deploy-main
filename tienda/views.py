from django.shortcuts import render
from .models import Producto

# Create your views here.

def home(request):
    """Vista de la página de inicio"""
    return render(request, 'tienda/home.html')


def catalog(request):
    """Vista del catálogo de productos"""
    productos = Producto.objects.all()
    
    # Filtrar por tipo si se proporciona en la query string
    tipo = request.GET.get('type')
    if tipo:
        productos = productos.filter(tipo=tipo)
    
    return render(request, 'tienda/catalog.html', {'productos': productos})


def index(request):
    """Vista antigua - redirige al catálogo"""
    productos = Producto.objects.all()
    return render(request, 'tienda/catalog.html', {'productos': productos})