from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from goodies.basket import Basket
from django.http import JsonResponse
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from goodies.forms import RegistrationForm, UserEditForm,AddressEditForm
from goodies.models import Category, Product, ProductDetailImage, UserBase
from goodies.tokens import account_activation_token
from django.contrib.auth.decorators import login_required


import json

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
     if request.user.is_authenticated:
        context = {}
        return render(request, 'goodies/my-account.html', context)
     else:
        registerForm = RegistrationForm()
        return render(request, 'goodies/register.html', {'form': registerForm})

    
def confirm(request):
    context = {}
    return render(request, 'goodies/activation_valid.html', context)

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


def account_register(request):
    if request.user.is_authenticated:
        return redirect('/my-account.html/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('goodies/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'goodies/activation_valid.html', {'email': user.email})
            # return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
        return render(request, 'goodies/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/my-account.html/')
    else:
        return render(request, 'goodies/activation_invalid.html')


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'goodies/edit_details.html', {'user_form': user_form})

@login_required
def edit_addresses(request):
    if request.method == 'POST':
        address_form = AddressEditForm(instance=request.user, data=request.POST)

        if address_form.is_valid():
            address_form.save()
    else:
        address_form = AddressEditForm(instance=request.user)

    return render(request,
                  'goodies/edit_addresses.html', {'address_form': address_form})
