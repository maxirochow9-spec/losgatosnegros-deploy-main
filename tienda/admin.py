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
	fields = ('producto', 'precio', 'cantidad', 'subtotal_display')

	def subtotal_display(self, obj):
		return obj.subtotal()
	subtotal_display.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'created_at', 'status', 'total', 'telefono')
	list_filter = ('status', 'created_at')
	search_fields = ('user__username', 'telefono', 'direccion')
	inlines = (PedidoItemInline,)
	readonly_fields = ('created_at',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'tipo', 'precio', 'stock', 'visible')
	list_filter = ('tipo', 'visible')
	search_fields = ('nombre',)
	list_editable = ('precio', 'stock', 'visible')
	actions = (hide_products, unhide_products, mark_out_of_stock, restock_products)


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio', 'subtotal')
	search_fields = ('producto__nombre', 'pedido__user__username')

