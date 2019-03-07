from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import View


# Create your views here.


class Services(View):
    def get(self, request):
        services = Service.objects.all()
        context = {
            'services': services,
            }
        return render(request, 'services/services_main.html', context=context)


class ServiceDetail(View):
    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug)
        context = {
            'service': service,
        }
        return render(request, 'services/service_detail.html', context=context)
