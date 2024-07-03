from django import template
from ec.models import CartModel
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter
def item_count(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(CartModel, cart_id=cart_id)
        total_quantity = cart.get_total_quantity()
        return total_quantity
    return 0