from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('about.html/',views.about,name="about"),
    path('cart.html/',views.cart,name="cart"),
    path('shop.html/',views.shop,name="shop"),
    path('contact-us.html/',views.contact,name="contact"),
    path('checkout.html/',views.checkout,name="checkout"),
    path('my-account.html/',views.account,name="account"),
    path('shop-detail.html/',views.shopDetail,name="shopdetail")
]