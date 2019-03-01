from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.http import JsonResponse, Http404
from decimal import Decimal
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import string
import random
from django.core.paginator import Paginator



#  initialize cart in current session
def create_cart(request):

    try:
        # define cart_id to request.session['cart_id']
        cart_id = request.session['cart_id']

        # matching cart_id variable with objects in Cart model
        cart = Cart.objects.get(id=cart_id)

        # define request.session['total'] as count of all items in current cart
        request.session['total'] = cart.items.count()

    # if it's a new session, construct new cart
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        # cart = Cart.objects.get(id=cart_id)
    return cart


def create_order_object(request, bound_form, cart):
    # collect all data to create order object
    new_order = Order.objects.create(
        items=cart,
        first_name=bound_form.cleaned_data['first_name'],
        last_name=bound_form.cleaned_data['last_name'],
        phone=bound_form.cleaned_data['phone'],
        email=bound_form.cleaned_data['email'],
        buying_type=bound_form.cleaned_data['buying_type'],
        address=bound_form.cleaned_data['address'],
        delivery_date=bound_form.cleaned_data['delivery_date'],
        comments=bound_form.cleaned_data['comments']
    )

    # if user is registered, save order.user to base, if anonymous user will be blank(or None)
    if request.user.is_authenticated:
        new_order.user = request.user
    new_order.save()
    new_order.total = cart.cart_total
    new_order.save()
    return new_order


def send_order_mail(order, email):

    # order details in context
    context = {
        'order': order,
    }

    # creating a list where will be a customers email, and staff email will append later
    mail_to = [email]
    staff = User.objects.filter(is_staff=True)
    for member in staff:
        mail_to.append(member.email)

    # render order details to html template
    html_content = render_to_string('shop/order_mail.html', context)

    # constructing email with all args
    mail = EmailMessage('Заказ в магазине СМПГЕО', html_content, 'job.shevtsov@ya.ru', mail_to)

    # switch mail body content type to html
    mail.content_subtype = 'html'

    # send mail
    mail.send()


# send mail to user with registration information
def send_reg_mail(username, password, email):

    # collect info to context
    context = {
        'username': username,
        'password': password,
        'email': email
    }

    # render context to html template
    html_content = render_to_string('shop/reg_mail.html', context)

    # construct email
    mail = EmailMessage('Регистрация в магазине СМПГЕО', html_content, 'job.shevtsov@ya.ru', [email])

    # define content type to html
    mail.content_subtype = 'html'

    # send it
    mail.send()


# logout user function
def logout_user(request):
    logout(request)
    return redirect('shop_main_url')


# Views start here


def shop_main(request):
    # cart initialize
    cart = create_cart(request)
    print(request._get_full_path)

    # get all categories, products, slider images to render them on page
    categories = Category.objects.all()
    products = Product.objects.all()
    slider_images = SliderImage.objects.all()

    # get products that are already in cart to disable add-to-cart buttons on this products
    # comparing items in cart with product titles
    item_titles = [item.product.title for item in cart.items.all()]
    cart_items = [product.title for product in products if product.title in item_titles]

    # add pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)


    context = {
        'categories': categories,
        'page': page, # products actually. Will be loop for product in page.object_list
        'slider_images': slider_images,
        'cart_items': cart_items,
        'cart': cart,
    }

    return render(request, 'shop/shop_main.html', context=context)


class ProductDetail(View):
    def get(self, request, slug):

        # get product by slug, define categories and initialize cart
        product = Product.objects.get(slug__iexact=slug)
        categories = Category.objects.all()
        current_category = product.category
        cart = create_cart(request)

        # filter products that are in cart as cart items to disable add-to-cart buttons
        item_titles = [item.product.title for item in cart.items.all()]
        cart_items = [product.title for product in Product.objects.all() if product.title in item_titles]

        # collect context and render to html
        context = {
            'categories': categories,
            'current_category': current_category,
            'product': product,
            'cart_items': cart_items,
            'cart': cart,
        }
        return render(request, 'shop/product_detail.html', context=context)


class CategoryDetail(View):
    def get(self, request, slug):
        # initialize cart and categories
        cart = create_cart(request)
        categories = Category.objects.all()

        # filter categories to find current category, and filter products by current category
        current_category = Category.objects.get(slug__iexact=slug)
        products = Product.objects.filter(category=current_category)

        # filter products that are in cart as cart items to disable add-to-cart buttons
        item_titles = [item.product.title for item in cart.items.all()]
        cart_items = [product.title for product in products if product.title in item_titles]

        # add pagination
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        # collect context and render to html
        context = {
            'categories': categories,
            'current_category': current_category,
            'page': page, # products, actually
            'cart_items': cart_items,
            'cart': cart,
        }
        return render(request, 'shop/category_detail.html', context=context)


# defining not cart itself, but cart view page
def cart(request):
    # initialize cart
    cart = create_cart(request)

    # recount method to count cart.cart_total depends on items and their price
    cart.recount_cart()

    # collect context and render to html
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context=context)


class AddToCart(View):
    def get(self, request):

        # initialize cart
        cart = create_cart(request)

        # get product slug from request
        slug = request.GET.get('slug')

        # using add_to_cart method to add new item to cart by product slug(see models to understand)
        cart.add_to_cart(request, slug)

        # response as json to add item dinamically using jquery ajax without page reload
        return JsonResponse({
            'cart_items_count': cart.items.count(),
            'cart_total': cart.cart_total,
            })


class DeleteFromCart(View):
    def get(self, request):

        # cart init
        cart = create_cart(request)

        # getting product slug
        slug = request.GET.get('slug')

        # find product by slug and cart item by product, then delete this item from cart
        product = Product.objects.get(slug__iexact=slug)
        item = CartItem.objects.filter(product=product)
        item.delete()

        # recount
        cart.recount_cart()

        # response as json to make all dinamic without page realoading
        return JsonResponse({
            'cart_items_count': cart.items.count(),
            'cart_total': cart.cart_total,
            })


# recount item qty in cart
class ChangeItemQty(View):
    def get(self, request):
        # cart init
        cart = create_cart(request)

        # get cart item qty and item id from get request by jquery
        qty = request.GET.get('qty')
        item_id = request.GET.get('item_id')

        # find cart item by id and change qty and item_total, save this to database
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()

        # recount cart
        cart.recount_cart()

        # return all data as json to ajax
        return JsonResponse({
            'cart_items_count': cart.items.count(),
            'item_total': cart_item.item_total,
            'cart_total': cart.cart_total,
            })


class MakeOrder(View):
    def get(self, request):
        # init cart and recount it, because we need to see total
        cart = create_cart(request)
        cart.recount_cart()

        # init user to fill some fields in form if is_authenticated, if not, render empty form
        u = request.user
        if u.is_authenticated:
            form = OrderForm(initial={'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email})
        else:
            form = OrderForm()

        # collect context and render
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'shop/make_order.html', context=context)


    def post(self, request):

        # init cart and recount
        cart = create_cart(request)
        cart.recount_cart()


        # get filled form from post request
        bound_form = OrderForm(request.POST)


        # if form.is_valid() create order, send mail and clean session
        if bound_form.is_valid():
            order = create_order_object(request, bound_form, cart)

            # get email from form adn send
            email = bound_form.cleaned_data['email']
            send_order_mail(order, email)

            del request.session['cart_id']
            del request.session['total']
            return render(request, 'shop/order_success.html', context={'order': order})
        return render(request, 'shop/make_order.html', context={'cart': cart, 'form': bound_form})


# view to see info about orders
class Account(View):
    def get(self, request):
        # cart init
        cart = create_cart(request)
        cart.recount_cart()

        # filter orders to see which are from this user and render them to html, if staff — get all
        if request.user.is_authenticated:
            if request.user.is_staff:
                orders = Order.objects.all().order_by('-id')
            else:
                orders = Order.objects.filter(user=request.user).order_by('-id')
        else:
            raise Http404("Page not found")

        context = {
            'cart': cart,
            'orders': orders,
        }
        return render(request, 'shop/account.html', context=context)


class Registration(View):

    # if request.method == 'GET' show empty form
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'shop/registration.html', context={'form': form})

    def post(self, request):

        # fill form from request.POST data
        bound_form = RegistrationForm(request.POST)
        if bound_form.is_valid():

            # save with commit=False and define password with set_password() method, otherwise it will not work ;)
            new_registration = bound_form.save(commit=False)
            new_registration.set_password(bound_form.cleaned_data['password'])

            # set some params to restrict new user and finally save it
            new_registration.active=True
            new_registration.staff=False
            new_registration.admin=False
            new_registration.save()

            # message about successfull registration
            messages.success(request, 'Вы успешно зарегистрировались в магазине SMPGEO.RU\nМы продублировали учетные данные вам на почту')

            # send mail to user about registration and redirect
            send_reg_mail(new_registration.username, bound_form.cleaned_data['password'], new_registration.email)
            return redirect('login_url')
        return render(request, 'shop/registration.html', context={'form': bound_form})


class Login(View):

    # if request.method == 'GET' show empty form
    def get(self, request):
        form = LoginForm()
        return render(request, 'shop/login.html', context={'form': form})

    def post(self, request):

        # fill form with request.POST data check if is_valid(), grab cleaned_data
        bound_form = LoginForm(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data['username']
            password = bound_form.cleaned_data['password']

            # try to authenticate user and check all validation statements
            user = authenticate(username=username, password=password, request=request)
            if user is None:
                return render(request, 'shop/login.html', context={'form': bound_form})
            if not user.is_active:
                return render(request, 'shop/login.html', context={'form': bound_form})

            # if it's alright, login user and redirect to main page
            login(request, user)
            return redirect('shop_main_url')
        return render(request, 'shop/login.html', context={'form': bound_form})


class PasswordReset(View):

    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'shop/password_reset.html', context={'form': form})

    def post(self, request):
        bound_form = PasswordResetForm(request.POST)
        if bound_form.is_valid():

            # filter user by email
            email = bound_form.cleaned_data['email']
            user = User.objects.get(email=email)

            # generating new password
            characters = string.ascii_letters + string.punctuation  + string.digits
            new_password = ''.join(random.choice(characters) for x in range(8))
            user.set_password(new_password)
            user.save()

            # sending an email
            send_reg_mail(user.username, new_password, email)
            messages.success(request, f'Мы отправили письмо с новым паролем на почту "{email}"')
            return redirect('login_url')
        return render(request, 'shop/password_reset.html', context={'form': bound_form})
