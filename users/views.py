import json
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm, SignUpForm, UpdateUserForm
from payment.forms import ShippingAddressForm
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, TemplateView, View
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from payment.models import ShippingAddress
from cart.cart import Cart
from store.models import Product
from payment.models import OrderItem

class LogInView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        client = form.get_user()
        login(self.request, client)

        # obtiene el carrito
        current_client = Profile.objects.get(user__id=self.request.user.id)
        saved_cart = current_client.old_cart
        if saved_cart:
            convert_cart = json.loads(saved_cart)
            cart = Cart(self.request)

            # Recuperamos los productos con sus IDs
            product_ids = list(convert_cart.keys())
            products = Product.objects.filter(id__in=product_ids)

            # Diccionario de productos
            product_dict = {str(product.id): product for product in products}
            
            for key, value in convert_cart.items():
                product = product_dict.get(key)
                if product:
                    cart.add(product=product, quantity=value)
        return response

# falta enviar un correo electronico el cual le avise al usuario que se a registrado correctamente.
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        client = form.save()
        login(self.request, client)
        # self.send_welcome_mail(client)
        return response
    
    # def send_welcome_mail(self, client):
    #     send_mail(
	# 		'Welcome to Reyvi page', 
	# 		'Thanks for joining Reyvi!', 
	# 		settings.EMAIL_HOST_CLIENT, 
	# 		[client.email],
	# 		fail_silently=False
	# 	)

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/my_account.html'

    def get_object(self):
        return self.request.user

class ManageAccountView(LoginRequiredMixin, TemplateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/manage_account.html'

    def get(self, request, *args, **kwargs):
        client = User.objects.get(id=request.user.id)
        form = self.form_class(instance=client)  # Inicializa el formulario
        return render(request, self.template_name, {'form': form, 'client': client})

class AccountUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/crud_account/account_update.html'

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

class ShippingAddressView(LoginRequiredMixin, View):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'users/address_book.html'

    def get_success_url(self):
        return reverse_lazy('my_account')

    def get(self, request, *args, **kwargs):
        addresses = ShippingAddress.objects.filter(client=request.user.client_profile)
        form = self.form_class()  # Inicializa el formulario vacío
        return render(request, self.template_name, {'form': form, 'addresses': addresses})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.client = request.user.client_profile
            shipping_address.save()
            return redirect(self.get_success_url())
        else:
            addresses = ShippingAddress.objects.filter(user=request.user)
            return render(request, self.get_success_url(), {'form': form, 'addresses': addresses})

class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = "users/crud_address/shippingAddress_update.html"

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def get_object(self):
        return ShippingAddress.objects.get(pk=self.kwargs['pk'])

class OrderView(View):
    model = OrderItem
    template_name = 'users/my_order.html'

    def get(self, request, *args, **kwargs):
        orders = OrderItem.objects.filter(client=request.user.client_profile)
        return render(request, self.template_name, {'orders': orders})