from django.contrib.auth.forms import AuthenticationForm
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from .models import ProductModel, CartItemModel, CartModel, OrderdModel, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from config.templates import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse, HttpResponseServerError
from ec.function import get_session
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from ec.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

class ProductListView(ListView):
    model = ProductModel
    template_name = 'list.html'


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'detail.html'


def redirect_site(request): # herokuデプロイ用
    return redirect('https://django2ec-d9aba89433ee.herokuapp.com/')


class CartListView(LoginRequiredMixin, ListView):
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

@login_required
def list_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)

    order = CartItemModel.objects.all()
    if order.exists():
        order_item = CartItemModel.objects.filter(name_id=item_pk).first()
        if not order_item:
            order, created = CartItemModel.objects.get_or_create(
                name = item,
                quantity = 1,
                cart_id = cart
                )
        else:
            order_item.quantity += 1
            order_item.save()
    else:
        order, created = CartItemModel.objects.get_or_create(
            name = item,
            quantity = quantity,
            cart_id = cart
        )
    return redirect('/list/')

@login_required
def detail_add_item(request):
    item_pk = request.POST.get('item_pk')
    item = get_object_or_404(ProductModel, pk=item_pk)
    quantity = int(request.POST.get('quantity'))
    cart = get_session(request)

    order = CartItemModel.objects.all()
    if order.exists():
        order_item = CartItemModel.objects.filter(name_id=item_pk).first()
        if not order_item:
            order, created = CartItemModel.objects.get_or_create(
                name = item,
                quantity = quantity,
                cart_id = cart
                )
        else:
            order_item.quantity += quantity
            order_item.save()
    else:
        order, created = CartItemModel.objects.get_or_create(
            name = item,
            quantity = quantity,
            cart_id = cart
            )
    return redirect(reverse('detail', kwargs={'pk': item_pk}))

@login_required
def remove_from_cart(request, pk):
    order_item = get_object_or_404(CartItemModel, pk=pk)
    order_item.delete()
    return redirect('/cart/')


class CheckOutView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = OrderdModel
    template_name = 'cart.html'
    fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder', 'credit_card_number', 'date_of_expiry', 'security_code', 'cart_id')
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        cart = get_object_or_404(CartModel, cart_id=cart_id)
        cart_item = CartItemModel.objects.filter(cart_id=cart_id)
        items_data = []

        for item in cart_item:
            item_data = {
                "name" : item.name.name,
                "quantity" : item.quantity,
                "price" : item.name.price,
                "sub_total_price" : item.get_sub_total_price()
            }
            items_data.append(item_data)
        items_data = json.dumps(items_data)
        
        self.object.items = items_data
        self.object.total_price = cart.get_total_price()
        self.object.save()
        cart_item.all().delete()

        context = {
            'items_data' : json.loads(items_data),
            'total_price' : self.object.total_price,
        }

        email = self.request.POST['email']
        # HTMLファイルを読み込む
        html_content = render_to_string('mail.html', context)
        # HTMLタグを取り除く
        text_content = strip_tags(html_content)
        send_mail(
            subject="ご購入頂きありがとうございます。",
            message=text_content,
            from_email="from@example.com",
            recipient_list=[email],
            html_message=html_content,
            )

        messages.success(self.request, "購入ありがとうございます")
        return super().form_valid(form)


class OrderIndexView(LoginRequiredMixin, ListView):
    model = OrderdModel
    template_name = 'orders.html'


    def get_queryset(self):
        return OrderdModel.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrderdModel
    template_name = 'order.html'


    def get_queryset(self):
        return OrderdModel.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["items"] = json.loads(obj.items)
        return context
    

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'login_signup.html'
    success_url = '/login/'

    def foem_valid(self, form):
        return super().form_valid(form)


class Login(LoginView):
    template_name = 'login_signup.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account.html'
    model = get_user_model()
    fields = ('username', 'password')
    success_url = '/account/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)