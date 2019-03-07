from django.shortcuts import render
from django.views.generic import View
from shop.models import *
from blog.models import *
from services.models import *


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
