from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    create_modified = models.DateTimeField(auto_now=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return self.user.username
    
class ShippingAddress(models.Model):
    phone = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='address')
    
    def __str__(self):
        return f'Shipping Address - {self.user.user.username}'