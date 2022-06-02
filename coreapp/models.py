from statistics import mode
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Status:
    STATUS =(("1", "Active"),("0", "De-active"),)
    YESNO =(("1", "Yes"),("0", "No"),)

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    slug = models.SlugField(max_length=500, default=None)
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, default='0', null=True)
    status = models.CharField(max_length = 20, choices = Status.STATUS, default = '1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length = 20, choices = Status.STATUS, default = '1')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='%(class)s_requests_created')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(max_length=500, default=None)
    title = models.CharField(max_length=500, default=None)
    desc_short = models.TextField()
    desc_long = RichTextField()
    specification = RichTextField()
    dashed_price = models.FloatField(null=True, blank=True, default=None)
    actual_price = models.FloatField(null=True, blank=True, default=None)
    stock_count = models.IntegerField(default=0)
    is_published = models.CharField(max_length = 20, choices = Status.YESNO, default = '0')
    is_in_sale = models.CharField(max_length = 20, choices = Status.YESNO, default = '0')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.title:
            self.title = self.title.strip()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=250, default=None)
    path = models.ImageField(upload_to="product/images", default='product/no-data.png')
    status = models.CharField(max_length = 20, choices = Status.STATUS, default = '1')

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Contact Form Filled by ' + self.name + "(" + self.email + ")"
