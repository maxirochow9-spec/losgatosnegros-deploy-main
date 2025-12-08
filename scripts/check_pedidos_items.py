from tienda.models import Pedido

print('Pedido_id | status | total_items | delivered_items | all_delivered')
for p in Pedido.objects.all().order_by('id'):
    total = p.items.count()
    delivered = p.items.filter(entregado=True).count()
    print(f'{p.id} | {p.status} | {total} | {delivered} | {delivered==total and total>0}')
