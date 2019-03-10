from django.shortcuts import render
from django.views.generic import View
from shop.models import *
from blog.models import *
from services.models import *
from .instagram_parser import *


# Create your views here.

class Landing(View):
    def get(self, request):
        products = Product.objects.get_random_three()
        posts = Post.objects.get_latest_posts()
        services = Service.objects.all()
        context = {
            'products': products,
            'posts': posts,
            'services': services,
        }
        return render(request, 'landing/landing_main.html', context=context)


class Contacts(View):
    def get(self, request):
        return render(request, 'landing/contacts.html', context=None)


class AboutUs(View):
    def get(self, request):
        return render(request, 'landing/about_us.html', context=None)

class Photogallery(View):
    def get(self, request):
        url = 'https://www.instagram.com/smp.geodesy/'
        images, links = get_data(url)
        images_and_links = zip(images, links)
        context = {
            'images_and_links': images_and_links,
        }
        return render(request, 'landing/photogallery.html', context=context)
