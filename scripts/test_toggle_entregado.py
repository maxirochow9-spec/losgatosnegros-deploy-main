from tienda.models import PedidoItem

print('Before', PedidoItem.objects.filter(entregado=True).count())
it = PedidoItem.objects.filter(entregado=False).first()
print('Test', getattr(it, 'id', None))
if it:
    it.entregado = True
    it.save()
    print('After save True', PedidoItem.objects.filter(entregado=True).count())
    it.entregado = False
    it.save()
    print('After save False', PedidoItem.objects.filter(entregado=True).count())
else:
    print('No item found to toggle')
