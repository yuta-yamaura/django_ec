from django.contrib import admin
from .models import ProductModel

# Register your models here.

class Postadmin(admin.ModelAdmin):
    list_editable = ('name', 'price', 'discription')
    fields = ('image', 'name', 'price', 'discription')
    list_display = ('image', 'name', 'price', 'created_at', 'updated_at', 'discription')
    list_display_links = ('image',)
    list_filter = ('name', 'price',)

admin.site.register(ProductModel, Postadmin)