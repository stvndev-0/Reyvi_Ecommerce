# Generated by Django 5.0.6 on 2024-09-27 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_remove_orderitem_user_remove_shippingaddress_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]