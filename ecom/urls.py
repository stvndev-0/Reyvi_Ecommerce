from django.contrib import admin
from django.urls import path, include
from ecom import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('accounts/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('inventory/', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DOOR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)