from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm

from .models import (
    Product,
    Order,
    Restaurant,
    Client,
    Driver,
    Review,
    Delivery,
)
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    RestaurantSerializer,
    ClientSerializer,
    DriverSerializer,
    ReviewSerializer,
    DeliverySerializer,
)

def registro(request):
    if request.user.is_authenticated:
        return redirect('perfil')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Changed to True so users can login immediately
            user.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'user/registro_page.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('perfil')
    
    # Check if Google login is available (allauth not configured, so always False)
    google_provider_enabled = False

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                welcome_name = user.get_full_name() if user.get_full_name() else user.username
                messages.success(request, f'¡Bienvenido, {welcome_name}!')
                return redirect('perfil')
            else:
                messages.error(request, 'Tu cuenta está inactiva. Por favor contacta al administrador.')
        else:
            messages.error(request, 'Credenciales incorrectas')
        return render(request, 'user/login_page.html', {'google_provider_enabled': google_provider_enabled})
    
    return render(request, 'user/login_page.html', {'google_provider_enabled': google_provider_enabled})


@login_required
def perfil(request):
    return render(request, 'user/perfil.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def index(request):
    # Show up to 20 restaurants on the home page
    restaurants = Restaurant.objects.all().order_by('-rating')[:20]
    return render(request, 'index.html', {'restaurants': restaurants})


def restaurant_list(request):
    """Display a list of all restaurants"""
    restaurants = Restaurant.objects.all().order_by('-rating')
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})


def order_list(request):
    """Display a list of all orders"""
    orders = Order.objects.all().order_by('-creation_date')
    return render(request, 'order_list.html', {'orders': orders})


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order model"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'restaurant', 'status', 'total']
    search_fields = ['client__name', 'restaurant__name']
    ordering_fields = ['creation_date', 'status', 'total']
    ordering = ['-creation_date']

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product model"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant', 'availability']
    search_fields = ['name']
    ordering_fields = ['price', 'availability']
    ordering = ['-price']
    
class RestaurantViewSet(viewsets.ModelViewSet):
    """ViewSet for Restaurant model"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'opening_time', 'closing_time']
    search_fields = ['name']
    ordering_fields = ['rating', 'opening_time', 'closing_time']
    ordering = ['-rating']

class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client model"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'email', 'registration_date']
    search_fields = ['name', 'email']
    ordering_fields = ['registration_date']
    ordering = ['-registration_date']
    

class DriverViewSet(viewsets.ModelViewSet):
    """ViewSet for Driver model"""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'email', 'availability']
    search_fields = ['name', 'email']
    ordering_fields = ['availability']
    ordering = ['-availability']
    
class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client', 'restaurant', 'order', 'rating']
    search_fields = ['comment']
    ordering_fields = ['creation_date', 'rating']
    ordering = ['-creation_date']
    
class DeliveryViewSet(viewsets.ModelViewSet):
    """ViewSet for Delivery model"""
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['order', 'driver', 'delivery_date', 'delivery_time', 'delivery_status']
    search_fields = ['order__client__name', 'driver__name']
    ordering_fields = ['delivery_date', 'delivery_time', 'delivery_status']
    ordering = ['-delivery_date']

def activate_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    return redirect('login')

    