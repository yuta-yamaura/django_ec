from django.db import models

# Create your models here.

class BaseMeta(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
     abstract = True


class ProductModel(BaseMeta):
    image = models.ImageField(upload_to='')
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    discription = models.CharField(max_length=20)

    class Meta:
       db_table = 'Ec_ProductModel'
    
    def __str__(self):
      return self.name


class CartModel(BaseMeta):
    cart_id = models.BigAutoField(primary_key=True)


class CartItemModel(BaseMeta):
    name = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart_id = models.ForeignKey(CartModel, on_delete=models.CASCADE)


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
    