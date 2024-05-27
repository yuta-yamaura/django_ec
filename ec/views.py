from .models import ProductModel
from django.views.generic import ListView, DetailView, View
from collections import OrderedDict
from config.templates import *
from django.shortcuts import render, redirect

# Create your views here.

class ProductListView(ListView):
    model = ProductModel
    template_name = 'list.html'


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'detail.html'

def redirect_site(request): # herokuデプロイ用
    return redirect('https://djangoec-294a4b387efb.herokuapp.com/')

class CartListView(ListView):
    model = ProductModel
    template_name = 'cart.html'
 
    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
        self.queryset = []
        self.total = 0
        self.total_quantity = 0
        for item_pk, quantity in cart['items'].items():
            obj = ProductModel.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
            self.total_quantity += obj.quantity
        cart['total'] = self.total
        self.request.session['cart'] = cart
        return super().get_queryset()
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = self.total
            context["total_quantity"] = self.total_quantity
        except Exception:
            pass
        return context
 
 
class AddCartView(View):
 
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            items = OrderedDict()
            cart = {'items': items}
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        request.session['cart'] = cart
        return redirect('/cart/')
 
 
def remove_from_cart(request, pk):
    cart = request.session.get('cart', None)
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')