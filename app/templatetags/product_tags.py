from django import template
import math
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