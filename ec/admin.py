from django.contrib import admin
from .models import ProductModel, OrderdModel, CartItemModel, CartModel

# Register your models here.

class ProductModeladmin(admin.ModelAdmin):
    list_editable = ('product', 'price', 'discription')
    fields = ('image', 'product', 'price', 'discription')
    list_display = ('image', 'product', 'price', 'created_at', 'updated_at', 'discription')
    list_display_links = ('image',)

admin.site.register(ProductModel, ProductModeladmin)


class CartItemModeladmin(admin.ModelAdmin):
    list_editable = ('product', 'quantity', 'cart')
    fields = ('product', 'quantity', 'cart')
    list_display = ('product', 'quantity', 'cart')
    list_display_links = None

admin.site.register(CartItemModel, CartItemModeladmin)


class CartModeladmin(admin.ModelAdmin):
    fields = ('cart',)
    list_display = ('cart',)
    list_display_links = None

admin.site.register(CartModel, CartModeladmin)


class OrderdModeladmin(admin.ModelAdmin):
    list_editable = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display_links = None

admin.site.register(OrderdModel, OrderdModeladmin)