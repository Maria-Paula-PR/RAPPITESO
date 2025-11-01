from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet, RestaurantViewSet, ClientViewSet, DriverViewSet, ReviewViewSet, DeliveryViewSet

# Crear un enrutador
router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'deliveries', views.DeliveryViewSet)

urlpatterns = [
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('orders/', views.order_list, name='order_list'),
    path('api/', include(router.urls)),
]
