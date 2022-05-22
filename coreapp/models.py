from statistics import mode
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    parent = models.IntegerField(default='0')
    status = models.IntegerField(default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    description = models.TextField()
    parent = models.IntegerField(default='0')
    status = models.IntegerField(default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=500)
    desc_short = models.TextField()
    desc_long = models.TextField()
    specification = models.TextField()
    stock_count = models.IntegerField(default=0)
    is_published = models.IntegerField(default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.title:
            self.title = self.title.strip()

class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=250, default=None)
    path = models.ImageField(upload_to="product/images", default='product/no-data.png')
    status = models.IntegerField(default='1')

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Contact Form Filled by ' + self.name + "(" + self.email + ")"
