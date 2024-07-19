from django.contrib import admin
from .models import ProductModel, OrderdModel, CartItemModel, CartModel, User
from django.contrib.auth.admin import UserAdmin
from ec.forms import UserCreationForm

# Register your models here.

class ProductModeladmin(admin.ModelAdmin):
    list_editable = ('product', 'price', 'discription')
    fields = ('image', 'product', 'price', 'discription')
    list_display = ('image', 'product', 'price', 'created_at', 'updated_at', 'discription')
    list_display_links = ('image',)


class CartItemModeladmin(admin.ModelAdmin):
    list_editable = ('product', 'quantity', 'cart')
    fields = ('product', 'quantity', 'cart_id')
    list_display = ('product', 'quantity', 'cart')
    list_display_links = None


class CartModeladmin(admin.ModelAdmin):
    fields = ('cart_id',)
    list_display = ('cart_id',)
    list_display_links = None


class OrderdModeladmin(admin.ModelAdmin):
    list_editable = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code', 'cart_id')
    fields = ('id', 'user', 'lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code', 'cart_id', 'total_price')
    list_display = ('id', 'user', 'lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code', 'cart_id', 'items', 'total_price')
    list_display_links = None


class UserModeladmin(admin.ModelAdmin):
    list_editable = ('username', 'password',)
    fields = ('id', 'username', 'password',)
    list_display = ('id', 'username', 'password',)
    list_display_links = None


class CustomUseradmin(UserAdmin):
    fieldsets = (
        (
            None, 
            {
                'fields': ('username', 'password', 'is_active', 'is_admin'),
            },
        ),
    )
    list_display = ('username', 'password', 'is_active', 'is_admin',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()

    add_fieldsets = (
        (
            None, 
            {
                'fields': ('username', 'password'),
            }
        )
    )

    add_form = UserCreationForm


admin.site.register(ProductModel, ProductModeladmin)
admin.site.register(CartItemModel, CartItemModeladmin)
admin.site.register(CartModel, CartModeladmin)
admin.site.register(OrderdModel, OrderdModeladmin)
admin.site.register(User, CustomUseradmin)