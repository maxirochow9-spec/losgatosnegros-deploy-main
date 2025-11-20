from django.db import models

# Create your models here.
class Producto(models.Model):
    TIPO_CHOICES = [
        ('alcoholic', 'Alcohólica'),
        ('non-alcoholic', 'No Alcohólica'),
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.user.username} - {self.status}'


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre} (${self.precio})'
