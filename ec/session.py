from ec.models import CartModel
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

def get_session(request):
    cart_id = request.session.get('cart_id', None)
    cart, created  = CartModel.objects.get_or_create(
        cart_id=cart_id
        )
    request.session['cart_id'] = cart.cart_id
    return cart