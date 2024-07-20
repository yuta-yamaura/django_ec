from django.db import models
from functools import reduce
from operator import add
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model

# Create your models here.

class BaseMeta(models.Model):
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
     abstract = True


class ProductModel(BaseMeta):
    image = models.ImageField(upload_to='')
    product = models.CharField(max_length=20)
    price = models.IntegerField()
    discription = models.CharField(max_length=20)

    class Meta:
       db_table = 'Ec_ProductModel'
    
    def __str__(self):
      return self.product


class CartModel(BaseMeta):
    cart_id = models.BigAutoField(primary_key=True)

    def __str__(self):
      return str(self.cart_id)
    
    def get_total_price(self):
      total_price = 0
      cart_items = self.cartitemmodel_set.all()
      total_price = reduce(lambda acc, cart_item: acc + cart_item.get_sub_total_price(), cart_items, 0)
      return total_price
    
    def get_total_quantity(self):
         total_quantity = 0
         cart_quantity = self.cartitemmodel_set.all()
         total_quantity = reduce(lambda acc, cart_item: acc + cart_item.quantity, cart_quantity, 0)
         return total_quantity


class CartItemModel(BaseMeta):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)

    def __str__(self):
      return str(self.product)

    def get_price(self):
       return self.product.price
    
    def get_sub_total_price(self):
       return self.product.price * self.quantity


class OrderdModel(BaseMeta):
    id = models.AutoField(primary_key=True)
    lastname = models.CharField(max_length=10)
    firstname = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    holder = models.CharField(max_length=20)
    credit_card_number = models.BigIntegerField()
    date_of_expiry = models.CharField()
    security_code = models.IntegerField()
    cart_id = models.ForeignKey(CartModel, on_delete=models.PROTECT)
    items = models.JSONField()
    total_price = models.IntegerField()

    class Meta:
       db_table = 'Ec_OrderdModel'
    