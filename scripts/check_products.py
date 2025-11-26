from tienda.models import Producto
for p in Producto.objects.all():
    print(p.id, p.nombre, p.imagen)
print('Total:', Producto.objects.count())
