from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.http import JsonResponse
from decimal import Decimal
from .forms import *
from django.contrib.auth import login, logout, authenticate



def create_cart(request):
    # connect authenticated user with his cart
    # user = request.user
    # if user.is_authenticated:
    #     try:
    #         cart = Cart.objects.get(user=user)
    #         request.session['total'] = cart.items.count()
    #         return cart
    #     except:
    #         cart = Cart()
    #         cart.save()
    #         cart_id = cart.id
    #         request.session['cart_id'] = cart_id
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
    new_order = bound_form.save(commit=False)
    if request.user.is_authenticated:
        new_order.user = request.user
    new_order.save()
    new_order.total = cart.cart_total
    new_order.items.add(cart)
    new_order.save()
    return new_order

class MakeOrder(View):
    def get(self, request):
        cart = create_cart(request)
        cart.recount_cart()
        u = request.user
        if u.is_authenticated:
            form = OrderForm(initial={'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email})
        else:
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
    cart = create_cart(request)
    cart.recount_cart()
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'cart': cart,
        'orders': orders,
    }
    return render(request, 'shop/account.html', context=context)

class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'shop/registration.html', context={'form': form})
    def post(self, request):
        bound_form = RegistrationForm(request.POST)
        if bound_form.is_valid():
            new_registration = bound_form.save(commit=False)
            new_registration.username = bound_form.cleaned_data['username']
            new_registration.set_password(bound_form.cleaned_data['password'])
            new_registration.first_name = bound_form.cleaned_data['first_name']
            new_registration.last_name = bound_form.cleaned_data['last_name']
            new_registration.email = bound_form.cleaned_data['email']
            new_registration.active=True
            new_registration.staff=False
            new_registration.admin=False
            new_registration.save()
            return render(request, 'shop/login.html', context={'new_registration': new_registration})
        return render(request, 'shop/registration.html', context={'form': bound_form})


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'shop/login.html', context={'form': form})
    def post(self, request):
        bound_form = LoginForm(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data['username']
            password = bound_form.cleaned_data['password']
            user = authenticate(username=username, password=password, request=request)
            if user is None:
                return render(request, 'shop/login.html', context={'form': bound_form})
            if not user.is_active:
                return render(request, 'shop/login.html', context={'form': bound_form})
            login(request, user)
            return redirect('index_url')
        return render(request, 'shop/login.html', context={'form': bound_form})

def logout_user(request):
    logout(request)
    return redirect('index_url')
