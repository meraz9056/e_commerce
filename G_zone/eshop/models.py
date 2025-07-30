from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=False,default='')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=False,default='')
    image = models.ImageField(upload_to='static/pimage')
    name = models.CharField(max_length=150)
    desc = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12,decimal_places=2,default='0')
    pre_price = models.DecimalField(max_digits=12, decimal_places=2,default='0')
    date =models.DateField(auto_now_add=True)
                
    def __str__(self):
         return self.name

class Slider(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    name = models.CharField(max_length=150)
    img = models.ImageField(upload_to='static/slider/images')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
         return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class Order(models.Model):
    image = models.ImageField(upload_to='static/order_image')
    product = models.CharField(max_length=150, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = price = models.DecimalField(max_digits=12,decimal_places=2,default='0')
    quantity = models.CharField(max_length=5)
    total = models.DecimalField(max_digits=12,decimal_places=2,default='0')
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default='0')
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product
