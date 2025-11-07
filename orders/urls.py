from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('orders/', views.order_list, name='order_list'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('activate/<int:user_id>/', views.activate_account, name='activate_account'),
]
