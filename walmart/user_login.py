from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import *
from app.EmailBackEnd import EmailBackEnd

def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = EmailBackEnd.authenticate(request,username=email,password=pwd)

        if user != None:
            login(request,user)
            return redirect('home')
        else:
            # messages.error(request,'Email and Password Are Invalid !')
            return redirect('login')

    return None

def REGISTER(request):
    if request.method == "POST":
        email = request.POST.get('em')
        pwd = request.POST.get('pass')
        fname = request.POST.get('first-name')
        lname = request.POST.get('last-name')
        uname = request.POST.get('Username')
        vender = request.POST.get('check-seller')
        shopname = request.POST.get('shop-name')
        shopurl = request.POST.get('shop-url')

        user = User(
            username=uname,
            first_name=fname,
            last_name=lname,
            email=email,
        )
        user.set_password(pwd)
        user.save()
        if vender == "seller":
            vender = Vendor(
                user=user,
                shop_name=shopname,
                shop_url=shopurl,
            )
            vender.save()
        # messages.success(request,'Email and Password Are Invalid !')
        return redirect('login')

    return None

def LOGOUT(request):
    logout(request)
    return redirect('login')

def PROFILE(request):
    vendor_check = Vendor.objects.all()
    data = {
        'vendor':vendor_check,
    }
    
    return render(request,'Main/myaccount.html',data)

def PROFILEUPDATE(request):
    
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        userid = request.user.id
        user = User.objects.get(id=userid)
        user.first_name = fname
        user.last_name = lname

        if pwd != None and pwd != "":
            user.set_password(pwd)
        user.save()
        return redirect('profile')
    
    return None

def WISHLIST(request):
    wishlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    vendor = Vendor.objects.all()
    data = {
        'vendor':vendor,
        'wishlist':wishlist,
    }
    return render(request,'Main/wishlist.html',data)

def ADDWISHLIST(request,slug):

    product = Product.objects.filter(slug=slug)
    if product.exists():
        check = Wishlist.objects.filter(user=request.user,product=product.first())
        if check.exists():
            return redirect('wishlist')
        else:
            wishlist = Wishlist(
                user=request.user,
                product=product.first(),
            )
            wishlist.save()
            return redirect('wishlist')
    else:
        return redirect('home')

def REMOVEWISHLIST(request,slug):
    product = Product.objects.filter(slug=slug)
    if product.exists():
        wishlist = Wishlist.objects.filter(user=request.user,product=product.first())
        wishlist.delete()
        return redirect('wishlist')
    else:
        return redirect('home')
