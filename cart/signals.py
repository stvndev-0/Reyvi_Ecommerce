from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
from datetime import datetime

# Automatizacion para fecha de envio
@receiver(pre_save, sender=Order)
def shipped_date_update(sender, instance, **kwargs):
    if instance.pk:
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = datetime.now()