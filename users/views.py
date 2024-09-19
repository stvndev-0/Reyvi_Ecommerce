import json
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm, SignUpForm, UpdateUserForm
from payment.forms import ShippingAddressForm
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, View
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from payment.models import ShippingAddress
from cart.cart import Cart
from store.models import Product

class LogInView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        # Autenticación del usuario
        response = super().form_valid(form)
        user = form.get_user()
        login(self.request, user)

        # 
        current_user = Profile.objects.get(user__id=self.request.user.id)
        saved_cart = current_user.old_cart
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

# Hacer que se el usuario acceda a su uenta una vez registrado, falta enviar un correo electronico
# el cual le avise al usuario que se a registrado correctamente.
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        self.send_welcome_mail(user)
        return response
    
    def send_welcome_mail(self, user):
        send_mail(
			'Welcome to Reyvi page', 
			'Thanks for joining Reyvi!', 
			settings.EMAIL_HOST_USER, 
			[user.email],
			fail_silently=False
		)

class AccountListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/my_account.html'

class ManageAccountView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/manage_account.html'

class AccountUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/crud_account/account_update.html'

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

class ShippingAddressView(LoginRequiredMixin, ListView):
    model = ShippingAddress
    template_name = 'users/address_book.html'

class ShippingAddressCreateView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = "users/crud_address/shippingAddress_create.html"

    def get_success_url(self):
        return reverse_lazy('my_account')
    
    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)

class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = "users/crud_address/shippingAddress_update.html"

    def get_success_url(self):
        return reverse_lazy('my_account')