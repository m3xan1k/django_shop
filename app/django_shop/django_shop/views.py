from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_shop(request):
    return redirect('index_url', permanent=True)
