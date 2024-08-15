# shop/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.db.models import Sum
from django.http import JsonResponse

def get_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def home(request):
    products = Product.objects.all()
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'shop/home.html', {
        'products': products,
        'cart_total_quantity': cart_total_quantity
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_total_quantity': cart_total_quantity
    })

def add_to_cart(request, product_id):
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
