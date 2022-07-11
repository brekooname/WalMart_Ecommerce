from django import template
import math

from app.models import SubCategory, Vendor
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

