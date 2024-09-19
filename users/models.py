from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    create_modified = models.DateTimeField(auto_now=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return self.user.username