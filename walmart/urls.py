"""walmart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views,user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HOME,name="home"),
    path('base/', views.BASE,name="base"),
    path('contact/', views.CONTACT,name="contact"),
    path('shop/', views.SHOP,name="shop"),
    path('about/', views.ABOUT,name="about"),
    path('dologin/', user_login.LOGIN,name="dologin"),
    path('accounts/register', user_login.REGISTER,name="register"),
    path('accounts/profile', user_login.PROFILE,name="profile"),
    path('accounts/wishlist', user_login.WISHLIST,name="wishlist"),
    path('accounts/wishlist/add/<slug>', user_login.ADDWISHLIST,name="add-wishlist"),
    path('accounts/wishlist/remove/<slug>', user_login.REMOVEWISHLIST,name="remove-wishlist"),
    path('accounts/cart', user_login.CART,name="cart"),
    path('accounts/cart/add', user_login.ADDCART,name="add-cart"),
    path('accounts/cart/remove/<slug>', user_login.REMOVECART,name="remove-cart"),
    path('accounts/profile/update', user_login.PROFILEUPDATE,name="profileupdate"),
    path('accounts/address', user_login.ADDRESS,name="address"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('logout/',user_login.LOGOUT,name='logout'),
    path('vendor/',views.VENDOR,name='vendor'),
    path('vendor/add-product/',views.ADDPRODUCT,name='add-product'),
    path('vendor/add-blog/',views.ADDBLOG,name='add-blog'),
    path('vendor/add-blog/delete/<id>',views.DELETEBLOG,name='delete-blog'),
    path('vendor/publish/<status>/<id>',views.PUBLISHPRODUCT,name='publish-product'),
    path('vendor/order/<status>/<id>',views.VENDORORDER,name='vendor-order'),
    path('vendor/order-bill/<id>',views.BILL,name='bill'),
    path('product/<cat>/<scat>/<slug>',views.DETAIL_PRODUCT,name='detail_product'),
    path('product/fillter-data', views.FILLTER_DATA,name='fillter_data'),
    path('product/review/<slug>', views.REVIEW,name='review'),
    path('product/<cat>/<scat>/<slug>/add-tags', views.ADDTAGS,name='addtags'),
    path('checkout', views.CHECKOUT,name='checkout'),
    path('verify_payment',views.VERIFY_PAYMENT,name='verify_payment'),
    path('search/',views.SEARCH,name='search'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
