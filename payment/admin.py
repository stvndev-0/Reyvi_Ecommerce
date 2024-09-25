from django.contrib import admin
from .models import ShippingAddress, OrderItem
from cart.models import Order

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fields = ['product', 'quantity', 'price']
    extra = 0

class OrderItemAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['client', 'full_name', 'email', 'shipping_address', 'amount_paid', 'date_ordered', 'shipped', 'date_shipped']
    inlines = (OrderItemInline,)

admin.site.unregister(Order)

admin.site.register(Order, OrderItemAdmin)