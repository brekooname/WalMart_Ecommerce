from math import prod
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from app.models import *
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.db.models import Avg

def BASE(request):
    
    
    return render(request,"base.html")

def HOME(request):
    category = Category.objects.all().order_by('id')[:10]
    product = Product.objects.filter(status="PUBLISH").order_by('-id')[:8]
    vendor = Vendor.objects.all()

    featured_product = Product.objects.filter(status="PUBLISH").annotate(avg = Avg('review__rate')).order_by('-avg')[:8]

    data = {
        'vendor':vendor,
        'category':category,
        'product':product,
        'featured_product':featured_product,
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
def PUBLISHPRODUCT(request,status,id):

    product = Product.objects.filter(id=id)

    if product.exists():
        if status == "DRAFT":
            p = Product.objects.get(id=id)
            p.status = "PUBLISH"
            p.save()
            return redirect('vendor')
        elif status == "PUBLISH":
            p = Product.objects.get(id=id)
            p.status = "DRAFT"
            p.save()
            return redirect('vendor')
        elif status == "DELETE":
            p = Product.objects.get(id=id)
            p.delete()
            return redirect('vendor')
    else:
        return redirect('home')

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

def FILLTER_DATA(request):

    product = request.GET.get('product')
    price = request.GET.get('price')

    if price:
        p = price.split(",")
        # print(p[0])
        product = Product.objects.filter(status="PUBLISH",price__gte=p[0],price__lte=p[1]).order_by('-id')[0:8]

    elif product:
        c = product.split("-")[0]
        id = product.split("-")[1]
        if c == "maincategory":
            product = Product.objects.filter(status="PUBLISH",maincategory__id__in=id).order_by('-id')[0:8]
        if c == "subcategory":
            product = Product.objects.filter(status="PUBLISH",subcategory__id__in=id).order_by('-id')[0:8]
        if c == "all":
            product = Product.objects.filter(status="PUBLISH").order_by('-id')
    else:
        product = Product.objects.filter(status="PUBLISH").order_by('-id')

    data  = {
        'product':product
    }
    t = render_to_string('ajax/product.html',data)

    return JsonResponse({'data': t})
    
def REVIEW(request,slug):
    product = Product.objects.filter(slug=slug)
    title = request.POST.get("title")
    cmt = request.POST.get("review")
    rate = request.POST.get("rate")

    if product.exists():
        user = request.user
        review = Review(
            user=user,
            product=product.first(),
            title=title,
            content=cmt,
            rate=rate,
        )
        review.save()
        return redirect('home')
    else:
        return redirect('home')

