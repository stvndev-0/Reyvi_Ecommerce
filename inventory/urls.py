from django.urls import path
from .views import InventoryView, ProductCreateView, ProductUpdateView, ProductDeleteView, SaleProduct, AddStockFormView

urlpatterns = [
    path('', InventoryView.as_view(), name='inventory'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/sale/', SaleProduct.as_view(), name='sale_product'),
    path('add-stock/', AddStockFormView.as_view(), name='add_stock'),
]