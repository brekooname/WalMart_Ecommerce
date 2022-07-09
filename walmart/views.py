from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import *
def BASE(request):
    
    return render(request,"base.html")

def HOME(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.all().order_by('id')[:8]

    data = {
        'vendor':vendor_check.first,
        'category':category,
        'product':product,
    }
    
    return render(request,"Main/home.html",data)

def CONTACT(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'vendor':vendor_check.first,
        'category':category,
    }
    return render(request,"Main/contact.html",data)

def SHOP(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'vendor':vendor_check.first,
        'category':category,
    }
    return render(request,"Main/shop.html",data)

def ABOUT(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'vendor':vendor_check.first,
        'category':category,
    }
    return render(request,"Main/about.html",data)

def VENDOR(request):
    vendor = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'vendor':vendor.first,
        'category':category,
    }
    return render(request,"vendor/vendor.html",data)

def ADDPRODUCT(request):
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    data = {
        'vendor':vendor_check.first,
        'category':category,
    }
    return render(request,"vendor/add-product.html",data)

def DETAIL_PRODUCT(request,cat,scat,slug):
    product = Product.objects.filter(slug=slug)
    vendor_check = Vendor.objects.filter(user=request.user)
    category = Category.objects.all().order_by('id')[:10]
    if product.exists():
        data = {
            'product':product.first,
            'vendor':vendor_check.first,
            'category':category,
        }
        return render(request,"product/product_detail.html",data)
    else:
        return redirect('home')

    
