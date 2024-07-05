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