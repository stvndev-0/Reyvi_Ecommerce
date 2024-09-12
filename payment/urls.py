from django.urls import path
from .views import PaymentSuccessTemplateView

urlpatterns = [
    path('payment_success/', PaymentSuccessTemplateView.as_view, name='payment_success'),
]