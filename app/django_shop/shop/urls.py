from django.urls import path
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index_url'),
    path('products/<str:slug>/', product_detail, name='product_detail_url'),
    path('category/<str:slug>/', category_detail, name='category_detail_url'),
    path('cart/', cart, name='cart_url'),
    path('add_to_cart/<str:slug>/', add_to_cart, name='add_to_cart_url'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
