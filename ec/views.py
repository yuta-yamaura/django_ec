from django.contrib.auth.forms import AuthenticationForm
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from .models import ProductModel, CartItemModel, CartModel, OrderdModel, PromotionCodeModel
from django.views.generic import ListView, DetailView, DetailView, CreateView
from django.views.generic.edit import FormView
from config.templates import *
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse, HttpResponseServerError
from ec.session import get_session
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ec.forms import PromtionForm

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


class CheckOutView(CreateView, SuccessMessageMixin):
    model = OrderdModel
    template_name = 'cart.html'
    fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder', 'credit_card_number', 'date_of_expiry', 'security_code', 'cart_id')
    success_url = reverse_lazy('list')


    def form_valid(self, form):
        cart = get_session(self.request)
        self.object = form.save(commit=False)
        cart_items = cart.cartitemmodel_set.all()
        items_data = []

        for item in cart_items:
            item_data = {
                "product" : item.product.product,
                "quantity" : item.quantity,
                "price" : item.product.price,
                "sub_total_price" : item.get_sub_total_price()
            }
            items_data.append(item_data)
        items_data = json.dumps(items_data)
        self.object.items = items_data
        self.object.total_price = cart.get_total_price()

        # promotion_codeが適用されてるかチェック
        code = self.request.session.get('code')
        if code is not None:
            discounted_price = cart.apply_code(code)
            code = PromotionCodeModel.objects.get(code=code)
            amount = code.amount
            self.object.code = code.code
            self.object.amount = amount
            self.object.total_price = discounted_price
            self.request.session.flush()
        self.object.save()
        cart_items.all().delete()

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


class OrderIndexView(ListView):
    model = OrderdModel
    template_name = 'orders.html'

    def get_queryset(self):
        return OrderdModel.objects.all().order_by('-created_at')


class OrderDetailView(DetailView):
    model = OrderdModel
    template_name = 'order.html'

    def get_queryset(self):
        return OrderdModel.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["items"] = json.loads(obj.items)
        return context


class PromtionView(FormView):
    model = PromotionCodeModel
    template_name = "cart.html"
    form_class = PromtionForm
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        cart = get_session(self.request)
        # herokuのエラー回避のため、セッションにはデフォルトで[]を指定
        session_promotion = self.request.session.get('code', [])
        input_code = form.cleaned_data['code']
        tmp_promo = PromotionCodeModel.objects.filter(code=input_code)
        if tmp_promo.exists():
            code = PromotionCodeModel.objects.get(code=input_code)
            # プロモーションコードのセッションがあって、is_usedがTrueのパターン
            if input_code in session_promotion and code.is_used is True:
                discounted_price = cart.apply_code(input_code)
                code = PromotionCodeModel.objects.get(code=input_code)
                context = {
                    'cart': cart,
                    'cart_items':cart.cartitemmodel_set.all(),
                    'discounted_price': discounted_price,
                    'code': code,
                    'amount': code.amount,
                    'is_used': code.is_used
                }
                return render(self.request, 'cart.html', context)
            # プロモーションコードが既に使用済みのパターン
            if code.is_used is True:
                return redirect('/cart/')
            # プロモーションコードを初めて使うパターン
            if code.is_used is False:
                discounted_price = cart.apply_code(input_code)
                code = PromotionCodeModel.objects.get(code=input_code)
                self.request.session['code'] = code.code
                context = {
                    'cart': cart,
                    'cart_items':cart.cartitemmodel_set.all(),
                    'discounted_price': discounted_price,
                    'code': code,
                    'amount': code.amount,
                    'is_used': code.is_used
                }
                code.is_used = True
                code.save()
                return render(self.request, 'cart.html', context)
        # プロモーションコードがDBのレコードと一致しないパターン
        return redirect('/cart/')


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)