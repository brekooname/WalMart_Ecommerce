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
    