

class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product,product_qty):
        product_id = product.id

        product_id = str(product.id)
        if product_id in self.basket.keys():
            productSession = self.basket.get(product_id)
            productQty = int(productSession['qty'])
            calculatedProductQty = product_qty + productQty
            productSession['qty'] = calculatedProductQty
        else:
            self.basket[product_id] = {'price': int(product.price),'qty': int(product_qty)}


        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())
