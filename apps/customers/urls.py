from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]