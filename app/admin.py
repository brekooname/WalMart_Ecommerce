from pyexpat import model
from django.contrib import admin
from app.models import *
# Register your models here.

class Sub_tublar(admin.TabularInline):
    model = SubCategory

class category_admin(admin.ModelAdmin):
    inlines = (Sub_tublar,)


admin.site.register(Vendor)
admin.site.register(Category,category_admin)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Review)