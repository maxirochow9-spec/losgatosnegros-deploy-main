from django.shortcuts import render
from django.http import HttpResponseServerError
from django.db import OperationalError
from .models import Producto
import sys
import traceback

# Create your views here.

def home(request):
    """Vista de la página de inicio"""
    return render(request, 'tienda/home.html')


def catalog(request):
    """Vista del catálogo de productos"""
    try:
        productos = Producto.objects.all()

        # Filtrar por tipo si se proporciona en la query string
        tipo = request.GET.get('type')
        if tipo:
            productos = productos.filter(tipo=tipo)

        return render(request, 'tienda/catalog.html', {'productos': productos})
    except OperationalError as oe:
        # Error de conexión a la base de datos: loggear y mostrar catálogo vacío
        print('OperationalError en vista catalog:', oe, file=sys.stderr)
        traceback.print_exc()
        return render(request, 'tienda/catalog.html', {'productos': [], 'db_error': True})
    except Exception as e:
        print('Error en vista catalog:', e, file=sys.stderr)
        traceback.print_exc()
        return HttpResponseServerError('Error interno en catálogo. Revisa los logs.')


def index(request):
    """Vista antigua - redirige al catálogo"""
    productos = Producto.objects.all()
    return render(request, 'tienda/catalog.html', {'productos': productos})