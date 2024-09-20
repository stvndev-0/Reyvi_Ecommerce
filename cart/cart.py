from users.models import Profile
from store.models import Product
import json
from decimal import Decimal

class Cart:
    def __init__(self, request):
        # Se asigna la sesion del usuario
        self.session = request.session

        self.request = request
        # Obtenemos el carrito de la sesion utilizando la clave 'session_key', 
        # si existe el carrito en la sesion, se almacena en la variable 'cart'
        cart = self.session.get('session_key')

        # Si es un usuario nuevo, no tiene una clave de sesion y tampoco carrito. 
        # Se crea un nuevo carrito vacio y se le asigna a la clave 'session_key'
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    # metodo para agregar productos al carrito. toma como parametro 
    # un objeto
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # Actualizar el carrito o agregar
        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty
        
        # Sin esta linea, los cambios en la sesion podrian no persistir
        self.session.modified = True

        # Guardamos el carrito en el perfil del usuario si esta autenticado
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = json.dumps(self.cart)
            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        # Obtenemos todos los ids del carrito
        product_ids = self.cart.keys()

        # Buscamos los los productos por el id en la bdd
        product = Product.objects.filter(id__in=product_ids)
        return product
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = quantity

        ourcart = self.cart

        # Actualizamos el carrito
        ourcart[product_id] = product_qty

        self.session.modified = True

    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def total(self, id=None):
        product_ids = self.cart.keys()
        if id is not None:
            product_ids = [id]
        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart

        total = Decimal('0.00')
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.discounted_price * int(value)
                    else:
                        total += product.price * int(value)
        return total
    
    def subTotal_products(self):
        updated_totals = {}
        for product_id, qty in self.cart.items():
            product = Product.objects.get(id=product_id)
            price = product.discounted_price if product.is_sale else product.price
            updated_totals[product_id] = price * Decimal(qty)
        return updated_totals
    
    def update_total(self, data):
        quantities  = data.get('quantities', {})

        updated_totals = {}

        for product_id, product_qty in quantities.items():
            self.update(product=product_id, quantity=product_qty)
            product_total = self.total(id=product_id)
            updated_totals[product_id] = product_total

        # calcula el total del carrito completo
        new_total = self.total()

        return {'updated_totals': updated_totals, 'new_total': new_total}