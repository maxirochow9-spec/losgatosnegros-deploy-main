from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.db import OperationalError
from .models import Producto
import sys
import traceback

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from .models import Pedido, PedidoItem
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next') or '/catalogo/'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'tienda/login.html', {'next': next_url})

    # GET
    next_url = request.GET.get('next', '/catalogo/')
    return render(request, 'tienda/login.html', {'next': next_url})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        next_url = request.POST.get('next') or '/catalogo/'

        # Validaciones básicas
        if not username or not password:
            messages.error(request, 'Nombre de usuario y contraseña son requeridos')
            return render(request, 'tienda/register.html', {'next': next_url})

        username = username.strip()
        # Username: sólo letras, números, guiones bajos y puntos; longitud mínima 3
        if len(username) < 3 or not re.match(r'^[\w.]+$', username):
            messages.error(request, 'El nombre de usuario debe tener al menos 3 caracteres y sólo puede contener letras, números, guiones bajos y puntos')
            return render(request, 'tienda/register.html', {'next': next_url})

        # Password: longitud mínima
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'tienda/register.html', {'next': next_url})

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'tienda/register.html', {'next': next_url})

        # Email: si fue provisto, validar formato y unicidad
        if email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'El correo electrónico no tiene un formato válido')
                return render(request, 'tienda/register.html', {'next': next_url})
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe una cuenta con ese correo')
                return render(request, 'tienda/register.html', {'next': next_url})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, 'tienda/register.html', {'next': next_url})

        # Crear usuario (la contraseña se guarda hasheada)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, 'Cuenta creada y sesión iniciada')
            return redirect(next_url)
        except Exception as e:
            logger.exception('Error creando usuario')
            messages.error(request, f'Error creando usuario: {e}')
            return render(request, 'tienda/register.html', {'next': next_url})

    # GET
    next_url = request.GET.get('next', '/catalogo/')
    return render(request, 'tienda/register.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('catalog')


@login_required
def create_order(request):
    """Endpoint para crear un pedido. Espera POST con JSON:
    {
      "items": [{"id": <producto_id>, "quantity": <n>}],
      "direccion": "...",
      "telefono": "..."
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json_load_request(request)
    except Exception as e:
        return JsonResponse({'error': 'JSON inválido', 'detail': str(e)}, status=400)

    items = data.get('items', [])
    direccion = data.get('direccion', '')
    telefono = data.get('telefono', '')

    if not items:
        return JsonResponse({'error': 'El pedido no tiene items'}, status=400)

    # Crear pedido y items dentro de una transacción
    with transaction.atomic():
        pedido = Pedido.objects.create(user=request.user, direccion=direccion, telefono=telefono, created_at=timezone.now())
        total = Decimal('0')

        for it in items:
            pid = it.get('id') or it.get('producto_id')
            qty = int(it.get('quantity') or it.get('qty') or 1)
            try:
                producto = Producto.objects.get(pk=pid)
            except Producto.DoesNotExist:
                transaction.set_rollback(True)
                return JsonResponse({'error': f'Producto no encontrado: {pid}'}, status=400)

            precio = producto.precio
            item_obj = PedidoItem.objects.create(pedido=pedido, producto=producto, precio=precio, cantidad=qty)
            total += (precio * qty)

        pedido.total = total
        pedido.save()

    return JsonResponse({'success': True, 'order_id': pedido.id, 'total': float(total)})


def json_load_request(request):
    import json
    body = request.body.decode('utf-8') if request.body else '{}'
    return json.loads(body)