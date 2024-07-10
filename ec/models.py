from django.db import models
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
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    discription = models.CharField(max_length=20)

    class Meta:
       db_table = 'Ec_ProductModel'
    
    def __str__(self):
      return self.name


class CartModel(BaseMeta):
    cart_id = models.BigAutoField(primary_key=True)

    def __str__(self):
      return str(self.cart_id)
    
    def get_total_price(self):
      total_price = 0
      cart_items = self.cartitemmodel_set.all()
      for order_item in cart_items:
         sub_total = order_item.get_sub_total_price()
         total_price += sub_total
      return total_price
    
    def get_total_quantity(self):
         total_quantity = 0
         cart_quantity = self.cartitemmodel_set.all()
         for order_item in cart_quantity:
            sub_quantity = order_item.quantity
            total_quantity += sub_quantity
         return total_quantity


class CartItemModel(BaseMeta):
    name = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart_id = models.ForeignKey(CartModel, on_delete=models.CASCADE)

    def __str__(self):
      return str(self.name)

    def get_price(self):
       return self.name.price
    
    def get_sub_total_price(self):
       return self.name.price * self.quantity


class UserManeger(BaseUserManager):
   def create_user(self, username, password=None):
       user = self.model(
           username=username,
       )

       user.set_password(password)
       user.save(using=self._db)
       return user

   def create_superuser(self, username, password=None):
       user = self.create_user(
           username,
           password=password,
       )
       user.is_admin = True
       user.save(using=self._db)
       return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManeger()
    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class OrderdModel(BaseMeta):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
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
