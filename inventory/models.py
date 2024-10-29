from django.db import models
from store.models import Product

# Create your models here.
class StockProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_id')
    quantity = models.IntegerField(default=0)