from django.contrib import admin
from .models import ProductModel, OrderdModel, CartItemModel, CartModel

# Register your models here.

class ProductModeladmin(admin.ModelAdmin):
    list_editable = ('name', 'price', 'discription')
    fields = ('image', 'name', 'price', 'discription')
    list_display = ('image', 'name', 'price', 'created_at', 'updated_at', 'discription')
    list_display_links = ('image',)

admin.site.register(ProductModel, ProductModeladmin)


class CartItemModeladmin(admin.ModelAdmin):
    list_editable = ('name', 'quantity', 'cart_id')
    fields = ('name', 'quantity', 'cart_id')
    list_display = ('name', 'quantity', 'cart_id')
    list_display_links = None

admin.site.register(CartItemModel, CartItemModeladmin)


class CartModeladmin(admin.ModelAdmin):
    fields = ('cart_id',)
    list_display = ('cart_id',)
    list_display_links = None

admin.site.register(CartModel, CartModeladmin)


class OrderdModeladmin(admin.ModelAdmin):
    list_editable = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display_links = None

admin.site.register(OrderdModel, OrderdModeladmin)