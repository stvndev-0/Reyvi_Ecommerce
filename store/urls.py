from django.urls import path
from .views import HomeListView, AboutView, ProductDetailView, CategoryListView, SearchView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>', CategoryListView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
]
