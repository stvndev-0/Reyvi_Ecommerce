from django.db import models
from users.models import Profile

# Create your models here.
class Order(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_order', blank=True, null=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - N°{self.pk} By {self.full_name}'