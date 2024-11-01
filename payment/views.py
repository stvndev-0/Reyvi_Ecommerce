from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse_lazy
from .forms import ShippingAddressForm, PaymentForm
from payment.models import ShippingAddress, OrderItem
from cart.models import Order
from cart.cart import Cart

# Create your views here.
class PaymentSuccessView(TemplateView):
    template_name = 'payment/payment_success.html'
    
class CheckoutView(FormView):
    model = ShippingAddress
    template_name = 'payment/checkout.html'
    form_class = ShippingAddressForm

    def get_context_data(self, **kwargs):
        response = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        response['sub_total'] = cart.subTotal_products()

        client = self.request.user
        if client.is_authenticated:
            # Usuario autenticado, se cargaran sus direcciones de envio, de lo contrario
            # no se mostrara nada
            
            shipping_user = ShippingAddress.objects.filter(client=client.client_profile, default=True)
            # comprobamos si existe
            # hay que agregar una validacion de que si tiene una direccion guardada se tome como predeterminada o si no pasarle un formulario para que rellene su direcion
            if shipping_user.exists():
                response['shipping_addresses'] = shipping_user
                response['shipping_form'] = ShippingAddressForm(instance=shipping_user.first())
            else:
                response['new_shipping_form'] = ShippingAddressForm()
        else:
            response['shipping_form'] = ShippingAddressForm()
        return response
    
    def form_valid(self, form):
        client = self.request.user
        shipping_id = self.request.POST.get('shipping_address')
        
        if client.is_authenticated:
            if not shipping_id:
                shipping_address = form.save(commit=False)
                shipping_address.client = client.client_profile
                shipping_address.save()
            else:
                shipping_address = ShippingAddress.objects.get(id=shipping_id)
                self.request.session['my_shipping'] = {
                    'full_name': shipping_address.full_name,
                    'email': shipping_address.email,
                    'phone': shipping_address.phone,
                    'address': shipping_address.address,
                    'city': shipping_address.city,
                    'state': shipping_address.state,
                    'country': shipping_address.country,
                    'zipcode': shipping_address.zipcode,
                }
        else:
            self.request.session['my_shipping'] = form.cleaned_data

        
        print('paso')
        self.request.session['checkout_valid'] = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('billing_info')

# Comentar estas dos ultimas
class BillingInfoView(FormView):
    form_class = PaymentForm
    template_name = 'payment/billing_info.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checkout_valid'):
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        response = super().get_context_data(**kwargs)
        # Recuperar los datos del formulario de la sesión
        response['my_shipping'] = self.request.session.get('my_shipping', {})
        print(response['my_shipping'])
        return response
    
    def form_valid(self, form):
        # Guardar la información del formulario
        
        shipping_info = form.save()
        # Emitir señal después de guardar el formulario
        self.request.session['checkout_valid'] = False
        return super().form_valid(form)
    
class ProcessOrderView(View):
    def post(self, request, *args, **kwargs):
        # Obtenemos las cosas del carrito
        cart = Cart(self.request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.total()

        my_shipping = self.request.session.get('my_shipping')
        full_name = my_shipping['full_name']
        email = my_shipping['email']
        shipping_address = f"{my_shipping['city']}\n{my_shipping['address']}\n{my_shipping['state']}\n{my_shipping['country']}\n{my_shipping['zipcode']}"
        amount_paid = totals

        if self.request.user.is_authenticated:
            client = self.request.user.client_profile
            # Creamos la orden y la guardamos
            create_order = Order(client=client, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            print(amount_paid)
            create_order.save()

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.discounted_price
                else:
                    price = product.price

                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=create_order.id, product_id=product_id, client=client, quantity=value, price=price)
                        create_order_item.save()
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.discounted_price
                else:
                    price = product.price

                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=create_order.id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

        for key in list(self.request.session.keys()):
            if key == "session_key":
                # Eliminamos la clave
                del self.request.session[key]
        
        return redirect(reverse_lazy('home'))

    def get(self, request, *args, **kwargs):
        # Redireccionar a la página de inicio si se accede mediante GET
        return redirect(reverse_lazy('home'))