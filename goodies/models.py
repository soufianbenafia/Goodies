from email.mime import image
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField()


class ProductDetail(models.Model):
    productID = models.OneToOneField(
        Product, on_delete=models.CASCADE, primary_key=True)
    availability = models.IntegerField()
    discription = models.TextField()


class ProductDetailImage(models.Model):
    productID = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    image = models.ImageField()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    totalAmount = models.DecimalField(max_digits=4, decimal_places=2)


class OrderItem(models.Model):
    productID = models.OneToOneField(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
