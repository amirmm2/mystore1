from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from shop.models import Product,Profile
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    cart = Cart(request)
    items = list(cart.__iter__())
    total = cart.get_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user_id=request.user.id).first()
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingAddressForm(request.POST or None)

    if request.method == "POST":
        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            if request.user.is_authenticated:
                shipping.user = request.user
            shipping.save()

            # ذخیره اطلاعات آدرس در سشن برای مرحله بعد
            request.session['user_shipping'] = {
                'shipping_fullname': shipping.shipping_full_name,
                'shipping_email': shipping.shipping_email,
                'shipping_phone': shipping.shipping_phone,
                'shipping_address': shipping.shipping_addy,
                'shipping_city': shipping.shipping_city,
                'shipping_state': shipping.shipping_state,
                'shipping_zipcode': shipping.shipping_zipcode,
                'shipping_country': shipping.shipping_country,
            }

            return redirect('confirm_order')
        else:
            messages.error(request, "❌ فرم آدرس معتبر نیست. لطفا دوباره بررسی کنید.")

    context = {
        'items': items,
        'total': total,
        'shipping_form': shipping_form
    }
    return render(request, 'payment/checkout.html', context)


def confirm_order(request):
    cart = Cart(request)
    items = list(cart.__iter__())
    total = cart.get_total()

    user_shipping = request.session.get('user_shipping')

    if not user_shipping:
        messages.error(request, "ابتدا باید آدرس خود را وارد کنید.")
        return redirect('checkout')

    context = {
        'items': items,
        'total': total,
        'shipping': user_shipping,
    }
    return render(request, 'payment/confirm_order.html', context)


def process_order(request):
    if request.method != "POST":
        messages.error(request, 'دسترسی به این صفحه امکان‌پذیر نمی‌باشد')
        return redirect('/')

    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.get_total()

    user_shipping = request.session.get('user_shipping')
    full_name = user_shipping['shipping_fullname']
    email = user_shipping['shipping_email']
    full_address = (
        f"{user_shipping['shipping_address']}\n"
        f"{user_shipping['shipping_city']}\n"
        f"{user_shipping['shipping_state']}\n"
        f"{user_shipping['shipping_zipcode']}\n"
        f"{user_shipping['shipping_country']}\n"
    )

    if request.user.is_authenticated:
        user = request.user
        new_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=full_address,
            amount_paid=total,
        )
    else:
        new_order = Order(
            full_name=full_name,
            email=email,
            shipping_address=full_address,
            amount_paid=total,
        )
    new_order.save()

    odr = get_object_or_404(Order, id=new_order.pk)

    for product in cart_products:
        prod = get_object_or_404(Product, id=product.id)
        price = prod.sale_price if prod.is_sale else prod.price
        for k, v in quantities.items():
            if int(k) == product.id:
                now_item = OrderItem(
                    order=odr,
                    product=prod,
                    price=price,
                    quantity=v,
                    user=request.user if request.user.is_authenticated else None,
                )
                now_item.save()
        cu=Profile.objects.filter(user__id=request.user.id)
        cu.update(old_cart='')

    # پاک کردن سشن
    if 'user_shipping' in request.session:
        del request.session['user_shipping']

    messages.success(request, 'سفارش ثبت شد')
    return redirect('payment_success')
