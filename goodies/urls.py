from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .forms import (UserLoginForm)

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
    path('activation_valid.html/',views.confirm,name="confirm"),
    path('login/', auth_views.LoginView.as_view(template_name='goodies/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('account/edit/', views.edit_details, name='edit_details'),
]
