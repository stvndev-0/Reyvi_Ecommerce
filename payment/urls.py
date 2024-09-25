from django.urls import path
from .views import PaymentSuccessView, CheckoutView, BillingInfoView, ProcessOrderView

urlpatterns = [
    path('payment_success/', PaymentSuccessView.as_view, name='payment_success'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('billing_info/', BillingInfoView.as_view(), name='billing_info'),
    path('process_order/', ProcessOrderView.as_view(), name='process_order'),
]