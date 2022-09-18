from django.urls import reverse
from django.db import models
from django_resized import ResizedImageField
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name

class Product(models.Model):
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    availability = models.IntegerField(default=10)
    discription = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    image = ResizedImageField(size=[370, 350])
    objects = models.Manager()
    products = ProductManager()

    def get_absolute_url(self):
        return reverse('shopdetail', args=[self.slug])


    def __str__(self):
        return self.name


class ProductDetailImage(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()

    # def __str__(self):
    #     return self.productID.name


class Order(models.Model):
    customer = models.ForeignKey(
        UserBase, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    totalAmount = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    productID = models.OneToOneField(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
