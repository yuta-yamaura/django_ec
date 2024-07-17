from .models import ProductModel, CartItemModel, CartModel
from django.views.generic import ListView, DetailView
from config.templates import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError
from ec.function import get_session

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
            cart_id = get_session(request)
            cart_id.cart_items = CartItemModel.objects.filter(cart_id=cart_id)
            total_price = cart_id.get_total_price()
            return render(request, 'cart.html', {'cart_id': cart_id, 'cart_items':cart_id.cart_items, 'total_price': total_price})
        except ObjectDoesNotExist:
            return render(request, 'cart.html', {'cart': None, 'cart_items':[], 'total_price': 0})


def list_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)

    cart_item = CartItemModel.objects.filter(cart=cart)
    if cart_item.exists():
        try:
            cart_item_pk = CartItemModel.objects.get(cart=cart, product_id=item_pk)
            if cart_item_pk in cart_item:
                cart_item_pk.quantity += 1
                cart_item_pk.save()
                return redirect('/list/')
        except CartItemModel.DoesNotExist:
            order, created = CartItemModel.objects.get_or_create(
                product = item,
                quantity = 1,
                cart = cart
                )
            return redirect('/list/')
    else:
        order, created = CartItemModel.objects.get_or_create(
        product = item,
        quantity = 1,
        cart = cart
        )
        return redirect('/list/')


def detail_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)

    cart_item = CartItemModel.objects.filter(cart=cart)
    if cart_item.exists():
        try:
            cart_item_pk = CartItemModel.objects.get(cart=cart, product_id=item_pk)
            if cart_item_pk in cart_item:
                cart_item_pk.quantity += quantity
                cart_item_pk.save()
                return redirect(reverse('detail', kwargs={'pk': item_pk}))
        except CartItemModel.DoesNotExist:
            order, created = CartItemModel.objects.get_or_create(
                product = item,
                quantity = quantity,
                cart = cart
                )
            return redirect(reverse('detail', kwargs={'pk': item_pk}))
    else:
        order, created = CartItemModel.objects.get_or_create(
        product = item,
        quantity = quantity,
        cart = cart
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