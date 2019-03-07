from django.shortcuts import render, get_object_or_404
from .models import *
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


class ObjectDetailMixin:

    model = None
    template = None

    def get(self, request, slug):

        # get product by slug, define categories and initialize cart
        cart = create_cart(request)
        categories = Category.objects.all()


        if self.model == Product:
            page = None
            product = get_object_or_404(self.model, slug__iexact=slug)
            current_category = product.category
            products = Product.objects.all()

        elif self.model == Category:
            product = None
            current_category = get_object_or_404(self.model, slug__iexact=slug)
            products = Product.objects.filter(category=current_category)

            # adding pagination for current category view
            paginator = Paginator(products, 3)
            page_number = request.GET.get('page', 1)
            page = paginator.get_page(page_number)


        # filter products that are in cart as cart items to disable add-to-cart buttons
        item_titles = [item.product.title for item in cart.items.all()]
        cart_items = [product.title for product in products if product.title in item_titles]

        context = {
                'categories': categories,
                'current_category': current_category,
                'product': product,
                'page': page,
                'cart_items': cart_items,
                'cart': cart,
            }


        return render(request, self.template, context=context)
