from ec.models import CartModel


def get_session(request):
    cart = request.session.get('cart', None)
    if cart is None:
        cart, created  = CartModel.objects.get_or_create(
            cart=cart
            )
        request.session['cart'] = cart
        return cart
    cart, created = CartModel.objects.get_or_create(
        cart=cart
        )
    return cart