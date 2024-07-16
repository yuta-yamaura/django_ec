from django.db import models

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
      for cart_item in cart_items:
         sub_total = cart_item.get_sub_total_price()
         total_price += sub_total
      return total_price
    
    def get_total_quantity(self):
         total_quantity = 0
         cart_items = self.cartitemmodel_set.all()
         for order_item in cart_items:
            sub_quantity = order_item.quantity
            total_quantity += sub_quantity
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
    lastname = models.CharField(max_length=10)
    firstname = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    holder = models.CharField(max_length=20)
    credit_card_number = models.IntegerField()
    date_of_expiry = models.DateField(auto_now=False)
    security_code = models.IntegerField()

    class Meta:
       db_table = 'Ec_OrderdModel'
    