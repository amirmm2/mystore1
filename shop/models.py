from django.contrib.auth import forms
from django.db import models
import datetime
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save







class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(max_length=20,blank=True)
    address1 = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=25, default='IRAN')
    old_cart= models.CharField(max_length=10, blank=True,null=True)


    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)






class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="", blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=15, decimal_places=0)

    # فیلد جدید تخفیف
    discount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    star=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return self.name



class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(default='',blank=False)
    phone= models.CharField(max_length=15,blank=False)
    date = models.DateTimeField(default=datetime.datetime.today())
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.product







