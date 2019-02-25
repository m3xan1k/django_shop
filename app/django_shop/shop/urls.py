from django.urls import path, include
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index_url'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail_url'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_url'),
    path('cart/', cart, name='cart_url'),
    path('add_to_cart/', AddToCart.as_view(), name='add_to_cart_url'),
    path('delete_from_cart/', DeleteFromCart.as_view(), name='delete_from_cart_url'),
    path('change_item_qty/', change_item_qty, name='change_item_qty_url'),
    path('make_order/', MakeOrder.as_view(), name='make_order_url'),
    path('order_success/', MakeOrder.as_view(), name='order_success_url'),
    path('account/', account, name='account_url'),
    path('registration/', Registration.as_view(), name='registration_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
