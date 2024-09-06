from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category/', default='default_img.jpg')

    def save(self, *args, **kwars):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwars)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='product/')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    is_sale = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def clean(self):
        if not self.is_sale and self.discount_percentage > 0:
            raise ValidationError('No se puede aplicar un descuento si el producto no está en oferta (is_sale=False).')
        if self.is_sale and self.discount_percentage == 0:
            raise ValidationError('Si el producto está en oferta (is_sale=True), se debe aplicar un porcentaje de descuento.')

    @property
    def discounted_price(self):
        discount = Decimal(1) - (Decimal(self.discount_percentage) / Decimal(100))
        discounted_price = self.price * discount
        return discounted_price.quantize(Decimal('0.01'), ROUND_HALF_UP)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.clean()  # Ejecuta la validación antes de guardar
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name