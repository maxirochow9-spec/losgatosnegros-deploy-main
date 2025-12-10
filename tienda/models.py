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
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    stock = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)

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
    entregado = models.BooleanField(default=False)

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f'{self.cantidad}x {self.producto.nombre} (${self.precio})'


# Señales para mantener el estado del Pedido en sincronía con los PedidoItem
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def _reevaluate_pedido_status(pedido):
    if pedido is None:
        return
    # Si no hay items pendientes (entregado=False) -> completed, si hay al menos uno -> pending
    if not pedido.items.filter(entregado=False).exists():
        if pedido.status != 'completed':
            pedido.status = 'completed'
            pedido.save()
    else:
        if pedido.status != 'pending':
            pedido.status = 'pending'
            pedido.save()


@receiver(post_save, sender=PedidoItem)
def pedidoitem_post_save(sender, instance, **kwargs):
    try:
        _reevaluate_pedido_status(instance.pedido)
    except Exception:
        pass


@receiver(post_delete, sender=PedidoItem)
def pedidoitem_post_delete(sender, instance, **kwargs):
    try:
        _reevaluate_pedido_status(instance.pedido)
    except Exception:
        pass
