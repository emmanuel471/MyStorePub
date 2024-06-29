from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('paypal-return',views.paypal_return, name='paypal-return'),
    path('paypal-cancel',views.paypal_cancel,name="paypal-cancel"),
    path('process_order', views.process_order, name="process_order"),
    path('billing_info', views.billing_info, name="billing_info"),
    path('shipped_dash', views.shipped_dash, name="shipped_dash"),
    path('not_shipped_dash', views.not_shipped_dash, name="not_shipped_dash"),
    path('order_history',views.order_history,name='order_history'),
]