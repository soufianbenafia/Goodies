

from decimal import Decimal
from goodies.models import Product


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
            self.basket[product_id] = {'price': int(product.price), 'qty': int(product_qty)}

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
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def getCompletePrice(self):
        completePrice = 0;
        basket = self.basket.copy()
        for item in basket.values():
            completePrice += Decimal(item['total_price'])
        return completePrice

    def getBasketFully(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
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



