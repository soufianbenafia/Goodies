from django.contrib import admin

from goodies.models import Category, UserBase, Order, OrderItem, Product, ProductDetailImage

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetailImage)
admin.site.register(Order)
admin.site.register(UserBase)
admin.site.register(OrderItem)
