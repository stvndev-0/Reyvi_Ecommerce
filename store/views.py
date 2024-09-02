from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

# Create your views here.
class HomeListView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products_sales'
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Obtenemos la categoría de la URL y filtramos los productos por esa categoría
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(category__slug=category_slug)