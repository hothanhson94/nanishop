from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('change_password/', views.change_password, name='change_password'),
]
