from django.db import models
from django.conf import settings
from shop.models import Product  # فرض بر اینه که مدل Product توی آپ shop هست

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"

    def total_items(self):
        """
        جمع تعداد کل آیتم‌ها در سبد خرید
        """
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        """
        جمع کل قیمت سبد خرید با توجه به تخفیف محصولات
        """
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        """
        محاسبه جمع کل این آیتم با توجه به تخفیف
        """
        price = self.product.sale_price if self.product.is_sale else self.product.price
        return price * self.quantity
