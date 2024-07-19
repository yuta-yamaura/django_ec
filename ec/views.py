from .models import ProductModel, CartItemModel, CartModel
from django.views.generic import ListView, DetailView
from config.templates import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError
from ec.session import get_session
from django.http import JsonResponse
import json

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
            cart = get_session(request)
            total_price = cart.get_total_price()
            return render(request, 'cart.html', {'cart': cart, 'cart_items':cart.cartitemmodel_set.all(), 'total_price': total_price})
        except ObjectDoesNotExist:
            return render(request, 'cart.html', {'cart': None, 'cart_items':[], 'total_price': 0})


def list_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)
    order, created = CartItemModel.objects.get_or_create(
        product = item,
        cart = cart
        )
    if not created:
        order.quantity += 1
        order.save()
    return redirect('/list/')


def detail_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)
    order, created = CartItemModel.objects.get_or_create(
        product = item,
        cart = cart
        )
    if created:
        order.quantity += (quantity - 1)
        order.save()
    if not created:
        order.quantity += quantity
        order.save()
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