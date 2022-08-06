from datetime import date
import json
from math import prod
from typing import Dict
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from app.models import *
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.db.models import Avg
import razorpay

from app.templatetags.product_tags import *
from .settings import *
from time import time
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def BASE(request):
    
    
    return render(request,"base.html")

def HOME(request):
    category = Category.objects.all().order_by('id')[:10]
    banner = Banner.objects.all().order_by('id')
    product = Product.objects.filter(status="PUBLISH").order_by('-id')[:8]
    
    vendor = Vendor.objects.all()

    featured_product = Product.objects.filter(status="PUBLISH").annotate(avg = Avg('review__rate')).order_by('-avg')[:8]
    best_seller = Product.objects.filter(status="PUBLISH").annotate(count = Count('order')).order_by('-count')[:8]
    special_offer = Product.objects.filter(status="PUBLISH").annotate(count = Count('order', distinct=True)).annotate(avg = Avg('review__rate')).filter(avg__gte=1).order_by('-count')[:4]

    data = {
        'vendor':vendor,
        'category':category,
        'product':product,
        'banner':banner,
        'featured_product':featured_product,
        'best_seller':best_seller,
        'special_offer':special_offer,
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
    order = Order.objects.filter(vendor=v).order_by('-id')
    pendingorder = Order.objects.filter(vendor=v,status="PENDING").count()
    shippinggorder = Order.objects.filter(vendor=v,status="SHIPPING").count()
    shipedorder = Order.objects.filter(vendor=v,status="SHIPED").count()
    
    data = {
        'vendor':vendor,
        'v':v,
        'category':category,
        'subcategory':subcategory,
        'categoryall':categoryall,
        'product':product,
        'order':order,
        'pendingorder':pendingorder,
        'shippinggorder':shippinggorder,
        'shipedorder':shipedorder,
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
def VENDORORDER(request,status,id):

    order = Order.objects.filter(id=id)

    if order.exists():
        if status == "SENT":
            order = Order.objects.get(id=id)
            order.status = "SHIPPING"
            order.save()
            return redirect('vendor')
        elif status == "CANCEL":
            order = Order.objects.get(id=id)
            order.status = "CANCEL"
            order.save()
            return redirect('vendor')
        elif status == "SHIPED":
            order = Order.objects.get(id=id)
            order.status = "SHIPED"
            order.save()
            return redirect('profile')
        elif status == "DELETE":
            order = Order.objects.get(id=id)
            order.delete()
            return redirect('home')
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


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def BILL(request,id):
    order = Order.objects.filter(id=id)
    data = {
        'order':order.first(),
    }
    pdf = render_to_pdf('vendor/bill.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

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

client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
def CHECKOUT(request):
    user = User.objects.get(id=request.user.id)
    cart = Cart.objects.filter(user=request.user)
    add = Address.objects.filter(user=request.user)
    total = cart_sub_total(cart)
    action = request.GET.get('action')
    order = None
    
    shipdate = date.today()
    if int(str(date.today())[8:]) > 23:
        shipdate = str(date.today())[0:7]+"-"+str(int(str(date.today())[8:]) + 7 - 30)
    else:
        shipdate = str(date.today())[0:7]+"-"+str(int(str(date.today())[8:]) + 7)
    print(shipdate)

    if action=='create_payment':
        amount = (total * 100)
        currency = "INR"

        notes = {
                "name":f'{user.first_name} {user.last_name}',
                "address":f'{add}',
                "city":add.first().subdistrict.name,
                "state":add.first().state.name,
                "postcode":add.first().pin,
                "email":user.email,
            }

        receipt = f"Walmart-{int(time())}"

        order = client.order.create({
            'receipt':receipt,
            'notes':notes,
            'amount':amount,
            'currency':currency,
        })
        for c in cart:
            pay = Order(
                order_id=order.get('id'),
                user=user,
                vendor=c.product.vendor,
                product=c.product,
                price=discount_price(c.product.price,c.product.discount) * c.quantity,
                quantity=c.quantity,
                size=c.size,
                color=c.color,
                shipdate=shipdate,
                status='PENDING',
                )
            pay.save()
    data = {
        'cart':cart,
        'order':order,
        'add':add.first(),
    }
    return render(request,'Main/checkout.html',data)

@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Order.objects.filter(order_id = razorpay_order_id)
            for p in payment:
                p.payment_id = razorpay_payment_id
                p.save()
            context = {
                'data':data,
                'payment':payment,
            }
            return render(request,'verify_payments/success.html',context)

        except:
            print('fail')
            print(json.loads(data['error[metadata]'])['order_id'])
            razorpay_order_id = json.loads(data['error[metadata]'])['order_id']
            payment = Order.objects.filter(order_id = razorpay_order_id)
            for p in payment:
                p.delete()
                
            return render(request,'verify_payments/fail.html')
            
    return None