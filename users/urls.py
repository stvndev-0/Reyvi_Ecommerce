from django.urls import path
from .views import AccountDetailView, ManageAccountView, AccountUserUpdateView, ShippingAddressView, ShippingAddressCreateView, ShippingAddressUpdateView, ShippingAddressDeleteView, OrderView, LogInView, SignUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', AccountDetailView.as_view(), name='my_account'),
    path('manage_account/', ManageAccountView.as_view(), name='manage_account'),
    path('manage_account/account_user_update/', AccountUserUpdateView.as_view(), name='user_update'),
    path('address_book/', ShippingAddressView.as_view(), name='address_book'),
    path('address_book/new_address/', ShippingAddressCreateView.as_view(), name='new_address'),
    path('address_book/update_address/<int:pk>/', ShippingAddressUpdateView.as_view(), name='update_address'),
    path('address_book/delete_address/<int:pk>/', ShippingAddressDeleteView.as_view(), name='delete_address'),
    path('order/', OrderView.as_view(), name='my_order'),
    path('login/', LogInView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
