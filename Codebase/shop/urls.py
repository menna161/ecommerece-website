# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration_complete/', views.registration_complete, name='registration_complete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),  # Update this line to point to the home view
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]