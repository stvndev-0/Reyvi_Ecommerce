from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, CreateView, UpdateView
from .models import StockProduct, Product
from .forms import AddProductForm, AddStockForm
from django.http import Http404

class StaffRequiredMixin(object):
    """
    Este Mixin requerirá que el usuario sea miembro del staff
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Page not found")
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
    

# Create your views here.
class InventoryView(StaffRequiredMixin, ListView):
    model = StockProduct
    template_name = 'inventory/inventory.html'

    def get_context_data(self, **kwargs):
        context = super(InventoryView, self).get_context_data(**kwargs)
        context['products'] = StockProduct.objects.all()
        return context

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'inventory/add_product.html'

    def get_success_url(self):
        return reverse_lazy('inventory')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('inventory')

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('inventory')

class SaleProduct(StaffRequiredMixin, UpdateView):
    model = Product
    fields = ['is_sale', 'discount_percentage']
    template_name = 'inventory/sale_product.html'
    success_url = reverse_lazy('inventory')
    
    def form_valid(self, form):
        if not form.cleaned_data.get('is_sale'):
            form.instance.discount_percentage = 0
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class AddStockFormView(StaffRequiredMixin, FormView):
    form_class = AddStockForm
    template_name = 'inventory/add_stock.html'
    success_url = reverse_lazy('inventory')
    
    def form_invalid(self, form):
        print('no paso')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
