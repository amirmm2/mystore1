from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import post_save
from django_jalali.db import models as jmodels
import jdatetime


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=250)
    shipping_phone = models.CharField(max_length=20, blank=True)
    shipping_addy = models.CharField(max_length=250, blank=True)      # آدرس کامل
    shipping_city = models.CharField(max_length=100, blank=True)      # شهر
    shipping_state = models.CharField(max_length=50, blank=True)      # استان
    shipping_zipcode = models.CharField(max_length=10, blank=True)    # کد پستی
    shipping_country = models.CharField(max_length=50, default='IRAN')# کشور
    shipping_old_cart = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'Shipping Address From {self.shipping_full_name}'


# سیگنال برای ایجاد آدرس پیش‌فرض هنگام ایجاد کاربر
def create_shipping_user(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)

post_save.connect(create_shipping_user, sender=User)


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'در انتظار پرداخت'),
        ('Processing', 'در حال پردازش'),
        ('Shipped', 'ارسال شده'),
        ('Delivered', 'تحویل داده شده'),
        ('Cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField(max_length=250)  # می‌تواند شامل آدرس + شهر + استان باشد
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    date_ordered = jmodels.jDateTimeField(default=jdatetime.datetime.now)
    last_update = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = getattr(Order.objects.get(id=self.pk), 'status', None)
            if hasattr(self, 'status') and old_status != self.status:
                self.last_update = jdatetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order From - {str(self.id)}'


class OrderItem(models.Model):
    STATUS_ORDER = [
        ('Pending', 'در انتظار پرداخت'),
        ('Processing', 'در حال پردازش'),
        ('Shipped', 'ارسال شده به پست'),
        ('Delivered', 'تحویل داده شد'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=50, choices=STATUS_ORDER, default='Pending')
    last_update = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        if self.user is not None:
            return f'Order Item - {str(self.id)} - for {self.user}'
        else:
            return f'Order Item - {str(self.id)}'
