from users.models import Profile
from store.models import Product

class Cart:
    def __init__(self, request):
        # Se asigna la sesion del usuario
        self.session = request.session

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
    def add(self, product):
        product_id = str(product.id)

        # verifica si el producto ya existe en el carrito. Si ya existe
        # no se realiza ninguna accion
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        
        # Esto asegura que django sepa que los datos de la sesion han cambiando
        # y necesita guardarlos.
        # Sin esta linea, los cambios en la sesion podrian no persistir
        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        # Obtenemos todos los ids del carrito
        product_ids = self.cart.keys()

        # Buscamos los los productos por el id en la bdd
        product = Product.objects.filter(id__in=product_ids)
        return product