from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.http import JsonResponse
from decimal import Decimal


# Create your views here.

def create_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    return cart

def index(request):
    cart = create_cart(request)
    categories = Category.objects.all()
    products = Product.objects.all()
    slider_images = SliderImage.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'slider_images': slider_images,
        'cart': cart,
    }
    return render(request, 'shop/index.html', context=context)

class ProductDetail(View):
    def get(self, request, slug):
        product = Product.objects.get(slug__iexact=slug)
        categories = Category.objects.all()
        cart = create_cart(request)
        context = {
            'categories': categories,
            'product': product,
            'cart': cart,
        }
        return render(request, 'shop/product_detail.html', context=context)

class CategoryDetail(View):
    def get(self, request, slug):
        cart = create_cart(request)
        categories = Category.objects.all()
        current_category = Category.objects.get(slug__iexact=slug)
        products = Product.objects.filter(category=current_category)
        context = {
            'categories': categories,
            'current_category': current_category,
            'products': products,
            'cart': cart,
        }
        return render(request, 'shop/category_detail.html', context=context)


def cart(request):
    cart = create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context=context)

class AddToCart(View):
    def get(self, request):
        cart = create_cart(request)
        slug = request.GET.get('slug')
        cart.add_to_cart(request, slug)
        return JsonResponse({'cart_total': cart.items.count()})

class DeleteFromCart(View):
    def get(self, request):
        cart = create_cart(request)
        slug = request.GET.get('slug')
        product = Product.objects.get(slug__iexact=slug)
        item = CartItem.objects.get(product=product)
        item.delete()
        return JsonResponse({'cart_total': cart.items.count()})
    # def post(self, request, slug):
    #     cart = create_cart(request)
    #     product = Product.objects.get(slug__iexact=slug)
    #     item = CartItem.objects.get(product=product)
    #     item.delete()
    #     return redirect('/cart/')

def change_item_qty(request):
    cart = create_cart(request)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    return JsonResponse({'cart_total': cart.items.count(), 'item_total': cart_item.item_total})
