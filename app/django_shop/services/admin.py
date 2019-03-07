from django.contrib import admin
from .models import *

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

admin.site.register(Service, ServiceAdmin)
