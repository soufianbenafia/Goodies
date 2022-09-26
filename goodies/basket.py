

from decimal import Decimal
from goodies.models import DeliveryOptions, Product
from django.core import serializers
import json
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, product_qty):
        product_id = product.id

        product_id = str(product.id)
        if product_id in self.basket.keys():
            productSession = self.basket.get(product_id)
            productQty = int(productSession['qty'])
            calculatedProductQty = product_qty + productQty
            productSession['qty'] = calculatedProductQty
        else:
            self.basket[product_id] = {'price': int(product.price), 'qty': str(product_qty)}

        self.save()
    
    def update(self, product, product_qty):
        product_id = product.id

        product_id = str(product.id)
        productSession = self.basket.get(product_id)
        productSession['qty'] = int(product_qty)
        
        self.save()

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def get_product(self, product_id):
        return Product.objects.get(id=product_id)


    

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = ProductSerializer(product).data
            # basket[str(product.id)]['product'] = json.loads(
            #     serializers.serialize('json', product.__dict__))[0]

        for item in basket.values():
            price = Decimal(item['price'])
            totalPrice = price * item['qty']
            item['total_price'] = str(totalPrice)
            yield item


    def getCompletePrice(self):
        completePrice = 0
        basket = self.basket.copy()
        for item in basket.values():
            completePrice += Decimal(item['total_price'])
        return completePrice


    def getTaxPrice(self):
        subTotal = self.getCompletePrice()
        tax = round((subTotal/100)*7, 2)
        return tax

    def getShippingCosts(self,deliveryprice=0):
        deliveryprice = 0.00

        if "purchase" in self.session:
            deliveryprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price


        subTotalTax = self.getCompletePrice() + self.getTaxPrice()
        amountFree  = 49
        if subTotalTax < amountFree:
            return Decimal(deliveryprice)
        else:
            return 0

    def getGrandTotal(self):
        return self.getCompletePrice() + self.getTaxPrice() + self.getShippingCosts()

    def getSubTotalWithTax(self):
        return self.getCompletePrice() + self.getTaxPrice()

    
    def getBasketFully(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['name'] = product.name
            basket[str(product.id)]['image'] = product.image.url
            basket[str(product.id)]['price'] = product.price

        for item in basket.values():
            item['price'] = str(item['price'])
            totalPrice = Decimal(item['price']) * Decimal(item['qty'])
            item['total_price'] = str(totalPrice)
        
        return basket


    def basket_update_delivery(self, deliveryprice=0):
        total = self.getSubTotalWithTax() + Decimal(deliveryprice)
        return total


