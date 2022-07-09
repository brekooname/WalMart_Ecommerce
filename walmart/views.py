from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import *
def BASE(request):
    return render(request,"base.html")

def HOME(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]

    data = {
        'vendor':vendor_check.first,
        'category':category,
    }
    
    return render(request,"Main/home.html",data)

def CONTACT(request):
    return render(request,"Main/contact.html")

def SHOP(request):
    return render(request,"Main/shop.html")

def ABOUT(request):
    return render(request,"Main/about.html")
