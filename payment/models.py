from django.db import models
from cart.models import Order
from store.models import Product
from users.models import Profile

# Create your models here.
class ShippingAddress(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_address', blank=True, null=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    
    def __str__(self):
        return f'Shipping Address - {self.full_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_order_item', null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'Order Item - N°{self.order.pk} By {self.order.full_name}'