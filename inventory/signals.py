from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product
from .models import StockProduct

# Insertamos el producto en la tabla StockProduct cuando se agrega un nuevo producto
@receiver(post_save, sender=Product)
def create_stock(sender, instance, created, **kwargs):
    if created:
        StockProduct.objects.create(product=instance)
    else:
        instance.product_id.save()