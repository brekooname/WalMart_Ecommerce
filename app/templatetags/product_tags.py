from django import template
import math
from django.db.models import Sum
from app.models import Product, SubCategory, Vendor
register = template.Library()

@register.simple_tag
def discount_price(price,discount):
    if discount == 0:
        return price
    p = price - (int(price) * int(discount) / 100)
    return int(p)

@register.simple_tag
def product_size(size):
    if size == None:
        return []
    
    s = str(size).split(",")
    return s

@register.simple_tag
def product_color(color):
    if color == None:
        return []
    
    c = str(color).split(",")
    return c

@register.simple_tag
def product_img_src(src):

    s = str(src)[0:7]
    if s == "/media/":
        return str(src)[7:]
    else:
        return src
    
@register.simple_tag
def check_vendor(user):

    vendor_check = Vendor.objects.filter(user=user)

    if vendor_check.exists():
        return True
    else:
        return False

@register.simple_tag
def product_label(discount):

    if int(discount) >= 30:
        return "hot"
    elif int(discount) >= 20:
        return "sale"
    else:
        return "new"
@register.simple_tag
def hot_deal_product():

    p = Product.objects.filter(status="PUBLISH",discount__gte=30).order_by('-id')[:4]

    return p

@register.simple_tag
def product_star_avg(review):
    r = review.aggregate(sum=Sum('rate'))
    count = review.count()
    if count > 0:
        avg = (100 * (r['sum'] / count)) / 5

        return avg
