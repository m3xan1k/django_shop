from django.shortcuts import render, redirect
from .models import *


# Create your views here.


def index(request):

    categories = Category.objects.all()
    products = Product.objects.all()
    slider_images = SliderImage.objects.all()
    cart = Cart.objects.first()
    context = {
        'categories': categories,
        'products': products,
        'slider_images': slider_images,
        'cart': cart,
    }
    return render(request, 'shop/index.html', context=context)

def product_detail(request, slug):
    categories = Category.objects.all()
    product = Product.objects.get(slug__iexact=slug)
    cart = Cart.objects.first()
    context = {
        'categories': categories,
        'product': product,
        'cart': cart,
    }
    return render(request, 'shop/product_detail.html', context=context)

def category_detail(request, slug):
    categories = Category.objects.all()
    category = Category.objects.get(slug__iexact=slug)
    products = Product.objects.filter(category=category)
    cart = Cart.objects.first()
    context = {
        'categories': categories,
        'category': category,
        'products': products,
        'cart': cart,
    }
    return render(request, 'shop/category_detail.html', context=context)


def cart(request):
    cart = Cart.objects.first()
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context=context)

def add_to_cart(request, slug):
    product = Product.objects.get(slug__iexact=slug)
    new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)[0]
    cart = Cart.objects.first()
    print()
    print(new_item)
    print()
    if new_item not in cart.items.all():
        # так как метод .get_or_create возвращает кортеж, а объект CartItem там идет под нулевым индексом, именно его нам надо получить. Можно сделать двойное присваивание new_item, _ = ... , или можно забрать [0] от кортежа или от new_item
        cart.items.add(new_item)
        cart.save()
        return redirect('/cart/')
    return redirect('/cart/')
