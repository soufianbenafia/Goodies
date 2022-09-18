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
    path('shop/<slug:slug>/',views.shopDetail,name="shopdetail"),
    path('add/',views.cart_add,name='cart_add'),
    path('update/',views.cart_update,name='cart_update'),
    path('delete/',views.cart_delete,name='cart_delete'),
    path('register.html/',views.account_register,name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),


]
