from shop.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # گرفتن سبد خرید از session و اطمینان از اینکه دیکشنری است
        cart = self.session.get('cart')
        if not cart or not isinstance(cart, dict):
            cart = self.session['cart'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
        """
        افزودن محصول به سبد خرید و ذخیره در DB
        """
        self._add_to_session(product, quantity)
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user)
            if profile.exists():
                db_cart = str(self.cart).replace("'", '"')
                profile.update(old_cart=db_cart)

    def add(self, product, quantity):
        """
        افزودن محصول به سبد خرید فقط در session
        """
        self._add_to_session(product, quantity)
        if self.request.user.is_authenticated:
            profile = Profile.objects.filter(user=self.request.user)
            if profile.exists():
                db_cart = str(self.cart).replace("'", '"')
                profile.update(old_cart=db_cart)

    def _add_to_session(self, product, quantity):
        """
        عملیات مشترک افزودن به session
        """
        product_id = str(product.id)
        quantity = int(quantity)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.session.modified = True

    def remove(self, product):
        """
        حذف یک محصول از سبد خرید
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def __iter__(self):
        """
        پیمایش محصولات سبد خرید
        """
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        products = sorted(products, key=lambda p: product_ids.index(str(p.id)))
        for product in products:
            quantity = self.cart.get(str(product.id), 0)
            price = product.sale_price if product.is_sale else product.price
            yield {
                'product': product,
                'quantity': quantity,
                'total_price': price * quantity
            }

    def get_prods(self):
        """
        لیست محصولات داخل سبد خرید
        """
        product_ids = list(self.cart.keys())
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        """
        برگرداندن تعداد هر محصول به صورت لیست مرتب
        """
        return [self.cart.get(str(p.id), 0) for p in self.get_prods()]

    def get_total(self):
        """
        محاسبه مجموع قیمت کل سبد خرید
        """
        total = 0
        for item in self.__iter__():
            total += item['total_price']
        return total

    def get_cart_quantity(self):
        """
        مجموع تعداد کل آیتم‌های داخل سبد خرید
        """
        return sum(self.cart.values())
