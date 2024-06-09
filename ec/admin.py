from django.contrib import admin
from .models import ProductModel, OrderdModel

# Register your models here.

class ProductModeladmin(admin.ModelAdmin):
    list_editable = ('name', 'price', 'discription')
    fields = ('image', 'name', 'price', 'discription')
    list_display = ('image', 'name', 'price', 'created_at', 'updated_at', 'discription')
    list_display_links = ('image',)

admin.site.register(ProductModel, ProductModeladmin)


class OrderdModeladmin(admin.ModelAdmin):
    list_editable = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    fields = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display = ('lastname', 'firstname', 'username', 'email', 'address1', 'address2', 'holder',  'credit_card_number', 'date_of_expiry', 'security_code')
    list_display_links = None

admin.site.register(OrderdModel, OrderdModeladmin)