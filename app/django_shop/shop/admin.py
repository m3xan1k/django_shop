from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = 'СМПГЕО интернет-магазин'
admin.site.site_title = 'Управление магазином СМПГЕО'


# class OrderDetailAdmin(admin.ModelAdmin):
#     change_list_template = 'shop/order_detail_change_list.html'
#     date_hierarchy = 'date'





class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )

def make_paid(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_paid.short_description = 'Пометить как оплаченные'

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_paid]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(SliderImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderDetail, OrderDetailAdmin)
