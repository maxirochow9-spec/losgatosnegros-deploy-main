from django.contrib import admin
from .models import Producto, Pedido, PedidoItem


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'precio', 'tipo')


class PedidoItemInline(admin.TabularInline):
	model = PedidoItem
	extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'total', 'status', 'created_at')
	inlines = [PedidoItemInline]
