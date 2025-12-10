# Generated migration for adding descripcion field to Producto

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_pedidoitem_entregado'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
    ]
