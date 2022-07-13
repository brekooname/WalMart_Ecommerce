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
    path('accounts/profile/update', user_login.PROFILEUPDATE,name="profileupdate"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('logout/',user_login.LOGOUT,name='logout'),
    path('vendor/',views.VENDOR,name='vendor'),
    path('vendor/add-product/',views.ADDPRODUCT,name='add-product'),
    path('vendor/publish/<status>/<id>',views.PUBLISHPRODUCT,name='publish-product'),
    path('product/<cat>/<scat>/<slug>',views.DETAIL_PRODUCT,name='detail_product'),
    path('product/fillter-data', views.FILLTER_DATA,name='fillter_data'),
    path('product/review/<slug>', views.REVIEW,name='review'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
