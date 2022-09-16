from django.shortcuts import get_object_or_404
from django.shortcuts import render
from goodies.basket import Basket
from django.http import JsonResponse
import json

from goodies.models import Category, Product, ProductDetailImage

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {"products": products, "categories": categories}
    return render(request, 'goodies/index.html', context)


def about(request):
    context = {}
    return render(request, 'goodies/about.html', context)


def cart(request):
    context = {}
    return render(request, 'goodies/cart.html', context)


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {"products": products, "categories": categories}
    return render(request, 'goodies/shop.html', context)


def shopDetail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = ProductDetailImage.objects.filter(productID=product.id)
    context = {"product": product, "images": images}
    return render(request, 'goodies/shop-detail.html', context)


def contact(request):
    context = {}
    return render(request, 'goodies/contact-us.html', context)


def checkout(request):
    context = {}
    return render(request, 'goodies/checkout.html', context)


def account(request):
    context = {}
    return render(request, 'goodies/my-account.html', context)


def cart_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print(request.POST.get('productid'))
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('qty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_qty=product_qty)

        json_object = json.dumps(basket.getBasketFully())
        print(json_object)
        response = JsonResponse({'qty': json_object})
        return response


def cart_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print(request.POST.get('productid'))
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('qty'))
        product = get_object_or_404(Product, id=product_id)
        basket.update(product=product, product_qty=product_qty)

        json_object = json.dumps(basket.getBasketFully())
        print(json_object)
        response = JsonResponse({'qty': json_object})
        return response


def cart_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print(request.POST.get('productid'))
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        json_object = json.dumps(basket.getBasketFully())
        response = JsonResponse({'qty': json_object})
        return response
