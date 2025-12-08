from django.contrib import admin
from .models import Producto, Pedido, PedidoItem


@admin.action(description='Ocultar los productos seleccionados')
def hide_products(modeladmin, request, queryset):
	queryset.update(visible=False)


@admin.action(description='Mostrar los productos seleccionados')
def unhide_products(modeladmin, request, queryset):
	queryset.update(visible=True)


@admin.action(description='Marcar productos seleccionados como Agotados (stock=0)')
def mark_out_of_stock(modeladmin, request, queryset):
	queryset.update(stock=0)


@admin.action(description='Reponer productos seleccionados (stock=10)')
def restock_products(modeladmin, request, queryset):
	queryset.update(stock=10)


class PedidoItemInline(admin.TabularInline):
	model = PedidoItem
	extra = 0
	readonly_fields = ('subtotal_display',)
	fields = ('producto', 'precio', 'cantidad', 'entregado', 'subtotal_display')

	def subtotal_display(self, obj):
		return obj.subtotal()
	subtotal_display.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'created_at', 'status', 'total', 'total_items', 'delivered_items', 'telefono')
	list_filter = ('status', 'created_at')
	search_fields = ('user__username', 'telefono', 'direccion')
	inlines = (PedidoItemInline,)
	readonly_fields = ('created_at',)

	def total_items(self, obj):
		return obj.items.count()
	total_items.short_description = 'Items'

	def delivered_items(self, obj):
		return obj.items.filter(entregado=True).count()
	delivered_items.short_description = 'Entreg.'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'tipo', 'precio', 'stock', 'visible')
	list_filter = ('tipo', 'visible')
	search_fields = ('nombre',)
	list_editable = ('precio', 'stock', 'visible')
	actions = (hide_products, unhide_products, mark_out_of_stock, restock_products)


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio', 'subtotal', 'entregado')
	list_editable = ('cantidad', 'precio', 'entregado')
	list_filter = ('entregado',)
	actions = []
	search_fields = ('producto__nombre', 'pedido__user__username')


@admin.action(description='Marcar items seleccionados como Entregados')
def mark_items_delivered(modeladmin, request, queryset):
	# Hacemos update en lote y luego actualizamos el estado de los pedidos afectados
	affected_pedidos = set(queryset.values_list('pedido_id', flat=True))
	queryset.update(entregado=True)
	from .models import Pedido
	for pid in affected_pedidos:
		pedido = Pedido.objects.filter(id=pid).first()
		if pedido:
			# Si todos los items están entregados, marcar pedido como completed
			if not pedido.items.filter(entregado=False).exists():
				pedido.status = 'completed'
				pedido.save()


@admin.action(description='Marcar items seleccionados como No entregados')
def mark_items_not_delivered(modeladmin, request, queryset):
	affected_pedidos = set(queryset.values_list('pedido_id', flat=True))
	queryset.update(entregado=False)
	from .models import Pedido
	for pid in affected_pedidos:
		pedido = Pedido.objects.filter(id=pid).first()
		if pedido:
			# Si existe al menos un item no entregado, marcar pedido como pending
			if pedido.items.filter(entregado=False).exists():
				pedido.status = 'pending'
				pedido.save()

# Añadir acciones al admin de PedidoItem
PedidoItemAdmin.actions = [mark_items_delivered, mark_items_not_delivered]

