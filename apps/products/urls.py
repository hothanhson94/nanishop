from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
]
