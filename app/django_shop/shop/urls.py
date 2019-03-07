from django.urls import path
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', shop_main, name='shop_main_url'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail_url'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_detail_url'),
    path('cart/', cart, name='cart_url'),
    path('add_to_cart/', AddToCart.as_view(), name='add_to_cart_url'),
    path('delete_from_cart/', DeleteFromCart.as_view(), name='delete_from_cart_url'),
    path('change_item_qty/', ChangeItemQty.as_view(), name='change_item_qty_url'),
    path('make_order/', MakeOrder.as_view(), name='make_order_url'),
    path('order_success/', MakeOrder.as_view(), name='order_success_url'),
    path('account/', Account.as_view(), name='account_url'),
    path('registration/', Registration.as_view(), name='registration_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('logout/', logout_user, name='logout_url'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset_url'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
