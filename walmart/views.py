from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import *
from django.core.files.storage import FileSystemStorage

def BASE(request):
    
    
    return render(request,"base.html")

def HOME(request):
    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.filter(status="PUBLISH").order_by('id')[:8]
    vendor = Vendor.objects.all()
    data = {
        'vendor':vendor,
        'category':category,
        'product':product,
    }
    
    return render(request,"Main/home.html",data)

def CONTACT(request):
    category = Category.objects.all().order_by('id')[:10]
    vendor = Vendor.objects.all()
    data = {
        'category':category,
    }
    return render(request,"Main/contact.html",data)

def SHOP(request):
    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.filter(status="PUBLISH").order_by('-id')
    vendor = Vendor.objects.all()
    data = {
        'vendor':vendor,
        'category':category,
        'product':product,
    }
    return render(request,"Main/shop.html",data)

def ABOUT(request):
    category = Category.objects.all().order_by('id')[:10]
    vendor = Vendor.objects.all()
    data = {
        'category':category,
    }
    return render(request,"Main/about.html",data)

def VENDOR(request):
    v = Vendor.objects.get(user=request.user)
    vendor = Vendor.objects.all()
    category = Category.objects.all().order_by('id')[:10]
    categoryall = Category.objects.all().order_by('id')
    subcategory = SubCategory.objects.all()
    activeproduct = Product.objects.filter(vendor=v,status="PUBLISH")
    product = Product.objects.filter(vendor=v).order_by('-id')
    data = {
        'vendor':vendor,
        'v':v,
        'category':category,
        'subcategory':subcategory,
        'categoryall':categoryall,
        'product':product,
        'activeproduct':activeproduct,
    }
    return render(request,"vendor/vendor.html",data)

def ADDPRODUCT(request):
    category = Category.objects.all().order_by('id')[:10]

    if request.method == "POST":
        maincategory = request.POST.get('maincategory')
        subcategory = request.POST.get('subcategory')
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        stock = request.POST.get('stock')
        size = request.POST.get('size')
        color = request.POST.get('color')
        status = request.POST.get('status')

        vendor = Vendor.objects.get(user=request.user)

        fss = FileSystemStorage()
        file1 = fss.save('product-image/1.jpg',image1)
        file2 = fss.save('product-image/2.jpg',image2)
        file_url1 = fss.url(file1)
        file_url2 = fss.url(file2)
        
        product = Product(
            vendor=vendor,
            maincategory=Category.objects.get(id=maincategory),
            subcategory=SubCategory.objects.get(id=subcategory),
            image1=file_url1,
            image2=file_url2,
            title=title,
            description=description,
            price=price,
            discount=discount,
            stock=stock,
            size=size,
            color=color,
            status=status,
        )
        product.save()
        return redirect('vendor')

    data = {
        'category':category,
    }
    return render(request,"vendor/add-product.html",data)

def DETAIL_PRODUCT(request,cat,scat,slug):
    vendor = Vendor.objects.all()
    product = Product.objects.filter(slug=slug)
    category = Category.objects.all().order_by('id')[:10]
    if product.exists():
        data = {
            'product':product.first,
            'category':category,
            'vendor':vendor,
        }
        return render(request,"product/product_detail.html",data)
    else:
        return redirect('home')

    
