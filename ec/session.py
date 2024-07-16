from ec.models import CartModel
from django.http import JsonResponse
from django.forms.models import model_to_dict

def get_session(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        cart, created = CartModel.objects.get_or_create(
            cart_id=cart_id
            )
        request.session['cart_id'] = cart.cart_id
        # cart_id = model_to_dict(cart_id)
        print(cart_id)
        print(type(cart_id))
        return cart_id
    cart, created = CartModel.objects.get_or_create(
        cart_id=cart_id
        )
    return cart_id