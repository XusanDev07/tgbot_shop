from django.contrib import admin

from .models import Category, Product, ProductColor, ProductImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductImage)