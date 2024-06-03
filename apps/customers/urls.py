from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='customers/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
]
