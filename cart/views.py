import json
from django.views.generic import TemplateView, View, DeleteView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from store.models import Product
from .cart import Cart

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
        response['total'] = cart.total()
        response['sub_total'] = cart.subTotal_products()
        return response

class CartAddView(View):

    def post(self, request):
        cart = Cart(request)

        data = json.loads(request.body)
        # Verificamos si la accion que se envio en la 
        # solicitud POST es igual a 'post'
        if data.get('action') == 'post':
            # Extraemos el 'product_id' de los datos de la solicitud POST
            # hacemos lo mismo pero con el 'product_qty'
            product_id = data.get('product_id')
            product_qty = data.get('product_qty')

            # Busca un producto con un ID especifico en la bdd, si
            # existe nos devolvera un objeto, de lo contrario devuelve un error 404 
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)

            cart_quantity = cart.__len__()

            response_data = {'qty': cart_quantity, 'messages': [f'{product.name} has been added to your cart.']}
            return JsonResponse(response_data)

class CartUpdateView(UpdateView):
    
    def post(self, request):
        cart = Cart(request)
        data = json.loads(request.body)

        if data.get('action') == 'post':
            updated_data = cart.update_total(data)
            response_data = {
                'updated_totals': updated_data['updated_totals'], 
                'new_cart_total': updated_data['new_total'],
                'messages': ['Cart updated.']
            }
            return JsonResponse(response_data)

class CartDeleteView(DeleteView):
    
    def post(self, request):
        cart = Cart(request)
        data = json.loads(request.body)
        
        if data.get('action') == 'post':
            product_id = data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            print(cart.delete(product=product))

            response_data = {'product_id': product_id, 'messages': [f'"{product.name}" removed.']}
            return JsonResponse(response_data)
            