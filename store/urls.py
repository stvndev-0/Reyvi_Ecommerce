from django.urls import path
from .views import HomeListView, ProductDetailView, CategoryListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>', CategoryListView.as_view(), name='category')
]
