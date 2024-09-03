from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    create_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return self.user.username