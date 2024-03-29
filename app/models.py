from ast import mod
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from numpy import product
from uuid import uuid4
import os

# Create your models here.

class Vendor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200,null=True)
    shop_url = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.user.username + " - " + self.shop_name

class Category(models.Model):
    image = models.ImageField(upload_to="maincategory",null=True)
    icon = models.CharField(max_length=200,null=True)
    title = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    main_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.main_category.title + " - " + self.title

class Product(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'product-image'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    sts = (
        ("PUBLISH","PUBLISH"),
        ("DRAFT","DRAFT"),
    )
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    maincategory = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    image1 = models.ImageField(upload_to=path_and_rename,null=True,blank=True)
    image2 = models.ImageField(upload_to=path_and_rename,null=True,blank=True)
    title = models.CharField(max_length=200,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True,default=0)
    stock = models.IntegerField(null=True,default=0)
    size = models.CharField(max_length=200,null=True,blank=True,default=None)
    color = models.CharField(max_length=200,null=True,blank=True,default=None)
    date = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title',unique=True,null=True,default=None)
    status = models.CharField(choices=sts,null=True,max_length=200)
    tags = models.CharField(null=True,max_length=200,blank=True)

    def __str__(self):
        return self.vendor.shop_name + " - " + self.title

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(null=True,max_length=200)
    content = models.TextField()
    rate = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username+" - "+self.product.title

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)
    color = models.CharField(null=True,max_length=200,blank=True)
    size = models.CharField(null=True,max_length=200,blank=True)

    def __str__(self):
        return self.user.username+" - "+self.product.title


class State(models.Model):
    name = models.CharField(null=True,max_length=200)
    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    name = models.CharField(null=True,max_length=200)
    def __str__(self):
        return self.name

class SubDistrict(models.Model):
    district = models.ForeignKey(District,on_delete=models.CASCADE,null=True)
    name = models.CharField(null=True,max_length=200)
    pin = models.IntegerField(null=True)
    def __str__(self):
        return  self.district.name +"-"+ self.name

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    street = models.CharField(null=True,max_length=200)
    pin = models.IntegerField(null=True)
    subdistrict = models.ForeignKey(SubDistrict,on_delete=models.CASCADE,null=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    sts = (
        ("PENDING","PENDING"),
        ("CANCEL","CANCEL"),
        ("SHIPPING","SHIPPING"),
        ("SHIPED","SHIPED"),
    )
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    price = models.IntegerField(null=True,default=0)
    quantity = models.IntegerField(null=True,blank=True)
    color = models.CharField(null=True,max_length=200,blank=True)
    size = models.CharField(null=True,max_length=200,blank=True)
    orderdate = models.DateTimeField(auto_now_add=True)
    shipdate = models.DateField()
    status = models.CharField(choices=sts,max_length=200,null=True,blank=True)

    def __str__(self):
        return self.vendor.shop_name + " - " + self.user.username + " - " + self.product.title

class Banner(models.Model):
    title = models.CharField(max_length=500,null=True)
    Description = models.CharField(max_length=500,null=True)
    image = models.ImageField(upload_to='banner',null=True)
    link = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=500,null=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=500,null=True)
    image = models.ImageField(upload_to='blog',null=True)
    date = models.DateField()

    def __str__(self):
        return self.title


