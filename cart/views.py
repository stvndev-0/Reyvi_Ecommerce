from django.views.generic import TemplateView, View, DeleteView, UpdateView
from django.urls import reverse_lazy
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
class CartSummaryListView(TemplateView):
    template_name = 'cart/cart_summary.html'

    def get_success_url(self):
        return reverse_lazy('cart_summary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_products'] = cart.get_products
        return context

class CartAddView(View):

    def post(self, request):
        # Asociamos la sesion del usuario al carrito, para 
        # que los productos guardados persistan
        cart = Cart(request)

        # Verificamos si la accion que se envio en la 
        # solicitud POST es igual a 'post'
        if request.POST.get('action') == 'post':
            # Extraemos el 'product_id' de los datos de la solicitud POST
            product_id = int(self.request.POST.get('product_id'))

            product = get_object_or_404(Product, id=product_id)
            
            # Se agrega el producto al carrito de compras utilizando
            # el metodo 'add' de la clase 'Cart'
            cart.add(product=product)

            cart_quantity = cart.__len__()

            response = JsonResponse({'qty': cart_quantity})
            return response

class CartDeleteView(DeleteView):
    pass

class CartUpdateView(UpdateView):
    pass