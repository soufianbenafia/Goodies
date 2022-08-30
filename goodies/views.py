from multiprocessing import context
from django.shortcuts import render

# Create your views here.

def home(request):
    context = {}
    return render(request,'goodies/index.html',context)

def about(request):
    context = {}
    return render(request,'goodies/about.html',context)

def cart(request):
    context = {}
    return render(request,'goodies/cart.html',context)

def shop(request):
    context = {}
    return render(request,'goodies/shop.html',context)

def contact(request):
    context = {}
    return render(request,'goodies/contact-us.html',context)

def checkout(request):
    context = {}
    return render(request,'goodies/checkout.html',context)

def account(request):
    context = {}
    return render(request,'goodies/my-account.html',context)

def shopDetail(request):
    context = {}
    return render(request,'goodies/shop-detail.html',context)