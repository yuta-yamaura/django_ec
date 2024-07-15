from ec.models import CartModel


def get_session(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        cart, created  = CartModel.objects.get_or_create(
            cart_id=cart_id
            )
        request.session['cart_id'] = cart.cart_id
        return cart
    else:
        cart, created = CartModel.objects.get_or_create(
            cart_id=cart_id
            )
        return cart