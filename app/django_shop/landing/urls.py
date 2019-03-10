from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Landing.as_view(), name='landing_url'),
    path('contacts/', Contacts.as_view(), name='contacts_url'),
    path('about_us/', AboutUs.as_view(), name='about_us_url'),
    path('photogallery/', Photogallery.as_view(), name='photogallery_url'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
