from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from users.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')  # Redirigir después de un login exitoso

    def form_valid(self, form):
        # Autenticación del usuario
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)
    
class RegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('my_account')

class AccountListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/my_account.html'