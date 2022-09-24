from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from .forms import (PwdResetConfirmForm, PwdResetForm, UserLoginForm)

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html/', views.about, name="about"),
    path('cart.html/', views.cart, name="cart"),
    path('shop.html/', views.shop, name="shop"),
    path('contact-us.html/', views.contact, name="contact"),
    path('checkout.html/', views.checkout, name="checkout"),
    path('my-account.html/', views.account, name="account"),
    path('shop/<slug:slug>/', views.shopDetail, name="shopdetail"),
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('register.html/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.account_activate, name='activate'),
    path('activation_valid.html/', views.confirm, name="confirm"),
    path('login/', auth_views.LoginView.as_view(template_name='goodies/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('account/edit/', views.edit_details, name='edit_details'),
    path('account/addresses/', views.edit_addresses, name='edit_addresses'),
    path('account/edit/delete', views.delete_user, name='delete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="goodies/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm/',
                                                                 email_template_name='goodies/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='goodies/password_reset_confirm.html',
                                                                                                success_url='/password_reset_complete/',
                                                                                                form_class=PwdResetConfirmForm), name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name="goodies/reset_status.html"), name='password_reset_done'),
    path('password_reset_complete/', TemplateView.as_view(
        template_name="goodies/reset_status.html"), name='password_reset_complete'),
    path("deliverychoices", views.deliverychoices, name="deliverychoices"),
    path("basket_update_delivery", views.basket_update_delivery,name="basket_update_delivery"),
    # path("delivery_address/", views.delivery_address, name="delivery_address"),
    # path("payment_selection/", views.payment_selection, name="payment_selection"),
    # path("payment_complete/", views.payment_complete, name="payment_complete"),
    # path("payment_successful/", views.payment_successful,name="payment_successful"),
]
