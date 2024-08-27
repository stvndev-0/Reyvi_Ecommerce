from django.shortcuts import render
from django.views import View
from .models import Product

# Create your views here.
class Home(View):
    template_name = 'store/home.html'

    def get(self, request):
        products_sales = Product.objects.all()
        return render(request, self.template_name, {'products_sales': products_sales})