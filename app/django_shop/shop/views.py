from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.http import JsonResponse
from decimal import Decimal
from .forms import *



def create_cart(request):
    # initialize cart from session
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()

    # if it's a new session, construct new cart
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        # cart = Cart.objects.get(id=cart_id)
    return cart


def index(request):
    # cart initialize
    cart = create_cart(request)

    # get all categories, products, slider images to render them on page
    categories = Category.objects.all()
    products = Product.objects.all()
    slider_images = SliderImage.objects.all()

    # get products that are already in cart to disable add-to-cart buttons on this products
    # comparing items in cart with product titles
    item_titles = [item.product.title for item in cart.items.all()]
    cart_items = [product.title for product in products if product.title in item_titles]

    context = {
        'categories': categories,
        'products': products,
        'slider_images': slider_images,
        'cart_items': cart_items,
        'cart': cart,
    }

    return render(request, 'shop/index.html', context=context)


class ProductDetail(View):
    def get(self, request, slug):
        product = Product.objects.get(slug__iexact=slug)
        categories = Category.objects.all()
        cart = create_cart(request)

        item_titles = [item.product.title for item in cart.items.all()]
        cart_items = [product.title for product in Product.objects.all() if product.title in item_titles]

        context = {
            'categories': categories,
            'product': product,
            'cart_items': cart_items,
            'cart': cart,
        }
        return render(request, 'shop/product_detail.html', context=context)


class CategoryDetail(View):
    def get(self, request, slug):
        cart = create_cart(request)
        categories = Category.objects.all()
        current_category = Category.objects.get(slug__iexact=slug)
        products = Product.objects.filter(category=current_category)

        item_titles = [item.product.title for item in cart.items.all()]
        cart_items = [product.title for product in products if product.title in item_titles]

        context = {
            'categories': categories,
            'current_category': current_category,
            'products': products,
            'cart_items': cart_items,
            'cart': cart,
        }
        return render(request, 'shop/category_detail.html', context=context)


def cart(request):
    cart = create_cart(request)
    cart.recount_cart()
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context=context)


class AddToCart(View):
    def get(self, request):
        cart = create_cart(request)
        slug = request.GET.get('slug')
        cart.add_to_cart(request, slug)
        return JsonResponse({
            'cart_items_count': cart.items.count(),
            'cart_total': cart.cart_total,
            })


class DeleteFromCart(View):
    def get(self, request):
        cart = create_cart(request)
        slug = request.GET.get('slug')
        product = Product.objects.get(slug__iexact=slug)
        item = CartItem.objects.filter(product=product)
        item.delete()
        # new_cart_total = Decimal(0.00)
        cart.recount_cart()
        return JsonResponse({
            'cart_items_count': cart.items.count(),
            'cart_total': cart.cart_total,
            })
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
    cart.recount_cart()
    return JsonResponse({
        'cart_items_count': cart.items.count(),
        'item_total': cart_item.item_total,
        'cart_total': cart.cart_total,
        })


def create_order_object(request, bound_form, cart):
    order = Order()
    order.user = request.user
    order.save()
    order.first_name = bound_form.cleaned_data['first_name']
    order.last_name = bound_form.cleaned_data['last_name']
    order.phone = bound_form.cleaned_data['phone']
    order.email = bound_form.cleaned_data['email']
    order.buying_type = bound_form.cleaned_data['buying_type']
    order.address = bound_form.cleaned_data['address']
    order.delivery_date = bound_form.cleaned_data['delivery_date']
    order.comments = bound_form.cleaned_data['comments']
    order.total = cart.cart_total
    order.items.add(cart)
    order.save()
    return order

class MakeOrder(View):
    def get(self, request):
        cart = create_cart(request)
        cart.recount_cart()
        form = OrderForm()
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'shop/make_order.html', context=context)


    def post(self, request):
        cart = create_cart(request)
        cart.recount_cart()
        bound_form = OrderForm(request.POST)
        if bound_form.is_valid():
            order = create_order_object(request, bound_form, cart)
            del request.session['cart_id']
            del request.session['total']
            return render(request, 'shop/order_success.html', context={'order': order})
        return render(request, 'shop/make_order.html', context={'cart': cart, 'form': bound_form})


def account(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    for order in orders:
        print(order.__dict__)
    return render(request, 'shop/account.html', context={'orders': orders})
