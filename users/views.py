from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')  # Redirigir después de un login exitoso

    def form_valid(self, form):
        # Autenticación del usuario
        response = super().form_valid(form)
        user = form.get_user()
        login(self.request, user)
        return response

# Hacer que se el usuario acceda a su uenta una vez registrado, falta enviar un correo electronico
# el cual le avise al usuario que se a registrado correctamente.
class RegisterView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        self.send_welcome_mail(user)
        return response
    
    def get_success_url(self):
        return reverse_lazy('my_account')
    
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