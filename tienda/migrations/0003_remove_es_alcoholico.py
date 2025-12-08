from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_pedido_pedidoitem'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE tienda_producto DROP COLUMN IF EXISTS es_alcoholico;
            """,
            reverse_sql="""
            ALTER TABLE tienda_producto ADD COLUMN IF NOT EXISTS es_alcoholico boolean DEFAULT false;
            """,
        ),
    ]
