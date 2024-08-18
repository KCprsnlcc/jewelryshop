# shop/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Sum
import logging
logger = logging.getLogger(__name__)

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not username or not password or not confirm_password:
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'success': 'User registered successfully'}, status=200)
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

def logout_user(request):
    logout(request)
    return redirect('home')

def get_cart(request):
    if not request.user.is_authenticated:
        return None

    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_id, user=request.user)
    return cart

def home(request):
    products = Product.objects.all()
    cart_total_quantity = 0
    if request.user.is_authenticated:
        cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    return render(request, 'shop/home.html', {
        'products': products,
        'cart_total_quantity': cart_total_quantity,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_total_quantity = 0
    if request.user.is_authenticated:
        cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_total_quantity': cart_total_quantity,
    })

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to add items to the cart.'}, status=403)
    
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_items = CartItem.objects.filter(cart=cart)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return JsonResponse({'cart_total_quantity': cart_total_quantity})

def update_cart_quantity(request):
    cart = get_cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()

    cart_items = CartItem.objects.filter(cart=cart)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return JsonResponse({'cart_total_quantity': cart_total_quantity})

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()

    cart_items = CartItem.objects.filter(cart=cart)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return JsonResponse({'cart_total_quantity': cart_total_quantity})
