from django.views.generic import TemplateView, View, DeleteView, UpdateView
from django.urls import reverse_lazy
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

# Create your views here.
class CartSummaryListView(TemplateView):
    template_name = 'cart/cart_summary.html'

    def get_success_url(self):
        return reverse_lazy('cart_summary')

    def get_context_data(self, **kwargs):
        response = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        response['cart_products'] = cart.get_products()
        response['quantities'] = cart.get_quants()
        response['totals'] = cart.total()
        return response

class CartAddView(View):

    def post(self, request):
        # Asociamos la sesion del usuario al carrito, para 
        # que los productos guardados persistan
        cart = Cart(request)

        # Verificamos si la accion que se envio en la 
        # solicitud POST es igual a 'post'
        if request.POST.get('action') == 'post':
            # Extraemos el 'product_id' de los datos de la solicitud POST
            # hacemos lo mismo pero con el 'product_qty'
            product_id = request.POST.get('product_id')
            product_qty = request.POST.get('product_qty')

            # Busca un producto con un ID especifico en la bdd, si
            # existe nos devolvera un objeto, de lo contrario devuelve un error 404 
            product = get_object_or_404(Product, id=product_id)
            
            # Se agrega el producto al carrito de compras utilizando
            # el metodo 'add' de la clase 'Cart'
            cart.add(product=product, quantity=product_qty)

            cart_quantity = cart.__len__()

            # Devolvera un mensaje
            response = JsonResponse({'qty': cart_quantity})
            return response

class CartUpdateView(UpdateView):
    
    def post(self, request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            product_qty = request.POST.get('product_qty')

            cart.update(product=product_id, quantity=product_qty)

            # Devolvera un mensaje
            response = JsonResponse({'qty': product_qty})
            return response

class CartDeleteView(DeleteView):
    
    def post(self, request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')

            cart.delete(product=product_id)

            # Devolvera un mensaje
            response = JsonResponse({'product_id': product_id})
            return response