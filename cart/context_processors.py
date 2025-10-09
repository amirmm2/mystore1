# cart/context_processors.py
def cart_total_qty(request):
    cart = request.session.get('cart')
    if not cart or not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart
    return {'cart_total_qty': sum(cart.values())}
