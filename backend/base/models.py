from django.db import models
from django import forms
from shop.models import *
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to="images/",default=None)
    def __str__(self):
        return self.name

class Product(models.Model):
    name= models.CharField(max_length=100)
    description=models.TextField()
    brand=models.CharField(max_length=100)
    price=models.FloatField()
    countInStock=models.IntegerField()
    image=models.ImageField(upload_to="images/")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Order(models.Model):
    CASABLANCA = 'Casablanca'
    RABAT = 'Rabat'
    SETTAT = 'Settat'

    CITY = (
    (CASABLANCA,'Casablanca'),
    (RABAT,'Rabat'),
    (SETTAT,'Settat'),
    )
    costumer=models.ForeignKey(Costumer,on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=12,default=CASABLANCA,choices=CITY,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

class AdminUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='admins/',blank=True)