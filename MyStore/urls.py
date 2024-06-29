
from django.contrib import admin
from django.urls import path, include
from .import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Store.urls')),
    path('cart/',include('cart.urls')),
    path('payment/',include('payment.urls')),
    path('',include('paypal.standard.ipn.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)