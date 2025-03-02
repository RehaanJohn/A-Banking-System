from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('main_menu/', views.main_menu, name='main_menu'),
    path('master_menu/', views.master_menu, name='master_menu'),
    path('logout/', views.logout, name='logout'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('balance/', views.balance, name='balance'),
]