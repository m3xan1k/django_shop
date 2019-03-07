from django.urls import path
from django.conf import settings
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path('', Services.as_view(), name='services_main_url'),
    path('services/<str:slug>/', ServiceDetail.as_view(), name='service_detail_url'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
