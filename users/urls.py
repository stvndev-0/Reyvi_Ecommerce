from django.urls import path
from .views import AccountListView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', AccountListView.as_view() ,name='my_account'),
    # path('/', .as_view() ,name=''),
    # path('/', .as_view() ,name=''),
    path('logout/', LogoutView.as_view(), name='logout'),
]
