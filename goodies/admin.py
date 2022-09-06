from django.contrib import admin

from goodies.models import Category, Customer, Order, OrderItem, Product, ProductDetailImage

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetailImage)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
