from django.urls import path
from .views import AccountListView, ManageAccountView, AccountUserUpdateView, ShippingAddressView, ShippingAddressCreateView,ShippingAddressUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', AccountListView.as_view(), name='my_account'),
    path('manage_account/', ManageAccountView.as_view(), name='manage_account'),
    path('manage_account/account_user_update/', AccountUserUpdateView.as_view(), name='user_update'),
    path('address_book/', ShippingAddressView.as_view(), name='address_book'),
    path('address_book/shippingAddress_create/', ShippingAddressCreateView.as_view(), name='address_create'),
    path('address_book/shippingAddress_update/<int:pk>', ShippingAddressUpdateView.as_view(), name='address_update'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
