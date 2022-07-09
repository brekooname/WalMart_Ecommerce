from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Vendor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200,null=True)
    shop_url = models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.user.username + " - " + self.shop_name