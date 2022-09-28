from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from goodies.basket import Basket, ProductSerializer
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from goodies.forms import RegistrationForm, UserEditForm, AddressEditForm,UserAddressForm
from goodies.models import Address, Category, DeliveryOptions, Order, OrderItem, Product, ProductDetailImage, Customer
from goodies.tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from paypalcheckoutsdk.orders import OrdersGetRequest
from django.core import serializers
import io
from rest_framework.parsers import JSONParser
from .paypal import PayPalClient

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
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/my-account.html/')
    else:
        return render(request, 'goodies/activation_invalid.html')


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    email = user.email
    user.save()
    logout(request)
    return render(request, 'goodies/delete_confirmation.html', {'email': email})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    print(user_form.errors)
    return render(request,'goodies/edit_details.html', {'user_form': user_form})


@login_required
def edit_addresses(request):
    if request.method == 'POST':
        address_form = AddressEditForm(
            instance=request.user, data=request.POST)

        if address_form.is_valid():
            address_form.save()
    else:
        address_form = AddressEditForm(instance=request.user)

    return render(request,
                  'goodies/edit_addresses.html', {'address_form': address_form})


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "goodies/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(
        customer=request.user).order_by("-default")

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "goodies/delivery_address.html", {"addresses": addresses})

@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(
            delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": basket.getShippingCosts(delivery_type.delivery_price)})
        return response


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "goodies/edit_addresses.html", {"form": address_form})

@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "goodies/addresses.html", {"addresses": addresses})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "goodies/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user,default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("delivery_address")

    return redirect("account:addresses")


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "goodies/payment_selection.html", {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

  

    for item in basket:
        serializer = ProductSerializer(data=item["product"])
        serializer.is_valid()
        print(serializer.errors)
        OrderItem.objects.create(order_id=order_id, product=serializer.save(), price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "goodies/payment_successful.html", {})


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "goodies/user_orders.html", {'orders':orders})
