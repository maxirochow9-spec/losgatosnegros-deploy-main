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
