from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
