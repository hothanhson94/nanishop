from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order_list/', views.order_list, name='order_list'),
    path('order_detai/', views.order_detail, name='order_detail'),
]