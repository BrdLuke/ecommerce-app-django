from django.contrib import admin

from main.models import Product, Payment

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_category', 'product_price', 'cart', 'product_quantity']
    list_filter = ['product_category', 'cart']

admin.site.register(Payment)