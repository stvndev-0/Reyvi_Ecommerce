from django.urls import path
from .views import AccountListView, AccountUserUpdateView, AccountInfoUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', AccountListView.as_view(), name='my_account'),
    path('account_user_update/', AccountUserUpdateView.as_view(), name='user_update'),
    path('account_info_update/', AccountInfoUpdateView.as_view(), name='info_update'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
