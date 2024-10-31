import json
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm, SignUpForm, UpdateUserForm
from payment.forms import ShippingAddressForm
from django.contrib.auth.models import User
from django.views.generic import View, DetailView, UpdateView, TemplateView, DeleteView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .tasks import send_welcome_mail
from .models import Profile
from payment.models import ShippingAddress
from cart.cart import Cart
from store.models import Product
from payment.models import OrderItem

class LogInView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
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
        return super().form_valid(form)

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('my_account')
    
    def form_valid(self, form):
        client = form.save()
        login(self.request, client)
        # send_welcome_mail(client)
        return super().form_valid(form)

class AccountDetailView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'users/my_account.html'

class ManageAccountView(LoginRequiredMixin, DetailView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/manage_account.html'

    def get(self, request, *args, **kwargs):
        client = request.user
        form = self.form_class(instance=client)  # Inicializa el formulario
        return render(request, self.template_name, {'form': form, 'client': client})

class AccountUserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/crud_account/account_update.html'
    success_url = reverse_lazy('manage_account')

    def get_object(self):
        return self.request.user

class ShippingAddressView(LoginRequiredMixin, DetailView):
    model = ShippingAddress
    template_name = 'users/address_book.html'

    def get(self, request, *args, **kwargs):
        addresses = ShippingAddress.objects.filter(client=request.user.client_profile)
        return render(request, self.template_name, {'addresses': addresses})

class ShippingAddressCreateView(LoginRequiredMixin, CreateView):
    form_class = ShippingAddressForm
    template_name = 'users/crud_address/address_form.html'
    success_url = reverse_lazy('address_book')

    def form_valid(self, form):
        shipping_address = form.save(commit=False)
        shipping_address.client = self.request.user.client_profile
        shipping_address.save()
        return super().form_valid(form)

class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = "users/crud_address/address_form.html"
    success_url = reverse_lazy('address_book')

    def get(self, request, *args, **kwargs):
        addresses = get_object_or_404(ShippingAddress, pk=self.kwargs['pk'])
        if request.user != addresses.client:
            return PermissionDenied
        form = self.form_class(instance=addresses)
        return render(request, self.template_name, {'form': form})

class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    model = ShippingAddress
    success_url = reverse_lazy('address_book')

    def post(self, request, *args, **kwargs):
        addresses = get_object_or_404(ShippingAddress, pk=self.kwargs['pk'])
        if request.user != addresses.client:
            return PermissionDenied
        addresses.delete()
        return redirect(self.success_url)

# Generar un token para el pedido
class OrderView(DetailView):
    model = OrderItem
    template_name = 'users/my_order.html'

    def get(self, request, *args, **kwargs):
        orders = OrderItem.objects.filter(client=request.user.client_profile)
        return render(request, self.template_name, {'orders': orders})