from django.shortcuts import render,redirect
from django.http import HttpResponse

def BASE(request):
    return render(request,"base.html")

def HOME(request):
    return render(request,"Main/home.html")

def CONTACT(request):
    return render(request,"Main/contact.html")

def SHOP(request):
    return render(request,"Main/shop.html")

def ABOUT(request):
    return render(request,"Main/about.html")
