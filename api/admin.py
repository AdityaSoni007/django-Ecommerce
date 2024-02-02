from django.contrib import admin
from .models import *



admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Buyer)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):       # we create this class to customize the appearance of the and behavior in admin view
    list_display = ['id','product_name','product_quantity']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):       # we create this class to customize the appearance of the and behavior in admin view
    list_display = ['id','name']
