from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
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