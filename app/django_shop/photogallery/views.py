from django.shortcuts import render
from django.views.generic import View
from .instagram_parser import *
from .models import *

# Create your views here.


class Photogallery(View):
    def get(self, request):
        data = InstaImage.objects.all()
        context = {
            'data': data,
        }
        return render(request, 'photogallery/photogallery.html', context=context)
