from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('tag/<str:slug>', TagList.as_view(), name='tag_list_url'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
