from django.contrib import admin
from django.urls import path, include
from ecom import settings
from django.conf.urls.static import static
from users.views import LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('my_account/', include('users.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DOOR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)