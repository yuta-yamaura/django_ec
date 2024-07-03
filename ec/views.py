from .models import ProductModel, CartItemModel, CartModel
from django.views.generic import ListView, DetailView
from config.templates import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError

# Create your views here.

class ProductListView(ListView):
    model = ProductModel
    template_name = 'list.html'


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'detail.html'


def redirect_site(request): # herokuデプロイ用
    return redirect('https://django2ec-d9aba89433ee.herokuapp.com/')


class CartListView(ListView):
    model = CartItemModel, CartModel
    template_name = 'cart.html'

    def get(self, request):
        try:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = get_object_or_404(CartModel, cart_id=cart_id)
            else:
                cart = CartModel()
                cart.save()
                request.session['cart_id'] = cart.cart_id
            cart_items = CartItemModel.objects.filter(cart_id=cart)
            total_price = cart.get_total_price()
            return render(request, 'cart.html', {'cart': cart, 'cart_items':cart_items, 'total_price': total_price})
        except ObjectDoesNotExist:
            return render(request, 'cart.html', {'cart': None, 'cart_items':[], 'total_price': 0})


def list_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart_id = request.session.get('cart_id', None)
    
    if cart_id is None:
        cart = CartModel.objects.create()
        request.session['cart_id'] = cart.cart_id
    else:
        cart = get_object_or_404(CartModel, cart_id=cart_id)

    order = CartItemModel.objects.all()
    if order.exists():
        order_item = CartItemModel.objects.filter(name_id=item_pk).first()
        if not order_item:
            order = CartItemModel.objects.create(name=item, quantity=1, cart_id=cart)
        else:
            order_item.quantity += 1
            order_item.save()
    else:
        name, created = CartItemModel.objects.get_or_create(
            name = item,
            cart_id = cart,
            quantity = quantity
)
    return redirect('/list/')


def detail_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart_id = request.session.get('cart_id')
    
    if not cart_id:
        cart = CartModel.objects.create()
        request.session['cart_id'] = cart.cart_id
    else:
        cart = get_object_or_404(CartModel, cart_id=cart_id)

    order = CartItemModel.objects.all()
    if order.exists():
        order_item = CartItemModel.objects.filter(name_id=item_pk).first()
        if not order_item:
            order = CartItemModel.objects.create(name=item, quantity=quantity, cart_id=cart)
        else:
            order_item.quantity += quantity
            order_item.save()
    else:
        name, created = CartItemModel.objects.get_or_create(
            name = item,
            cart_id = cart,
            quantity = quantity
)
    return redirect(reverse('detail', kwargs={'pk': item_pk}))


def remove_from_cart(request, pk):
    order_item = get_object_or_404(CartItemModel, pk=pk)
    order_item.delete()
    return redirect('/cart/')

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)