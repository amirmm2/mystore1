from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        qty = int(request.POST.get('product_qty', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = qty
        else:
            cart_item.quantity += qty
        cart_item.save()

        return JsonResponse({
            'item_qty': cart_item.quantity,
            'item_total_price': cart_item.total_price(),
            'total_qty': cart.total_items(),
            'total_price': cart.total_price()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass

        return JsonResponse({
            'total_qty': cart.total_items(),
            'total_price': cart.total_price()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def update_cart(request, product_id):
    """
    بروزرسانی تعداد یک محصول در سبد خرید
    """
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        qty = int(request.POST.get('product_qty', item.quantity))
        item.quantity = qty
        item.save()
        return JsonResponse({
            'item_qty': item.quantity,
            'item_total_price': item.total_price(),
            'total_qty': cart.total_items(),
            'total_price': cart.total_price()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def clear_cart(request):
    """
    خالی کردن کل سبد خرید
    """
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return JsonResponse({'total_qty': 0, 'total_price': 0})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def cart_summary(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    return render(request, 'cart/cart_summary.html', {
        'cart': cart,
        'items': items,
        'total_price': cart.total_price()
    })


@login_required
def checkout(request):
    """
    صفحه پرداخت
    """
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    if not items.exists():
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect('cart_summary')
    total_price = cart.total_price()
    return render(request, 'payment/checkout.html', {'cart': cart, 'items': items, 'total_price': total_price})
