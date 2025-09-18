"""
URL configuration for classicelectricals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, re_path
from app.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('product/', product, name='product'),
    path('allcategories/', allcategories, name='allcategories'),
    path('category/<int:pid>?', category, name='category'),
    path('minivisioncameras/', minivisioncameras, name='minivisioncameras'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('contact/send/', contact_email, name='contact_email'),
    path('request/', requestq, name='requestq'),
    path('request/send/', request_email, name='request_email'),

    path('adminlogin/', admin_login, name='adminlogin'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('addproductcategory/', addproductcategory, name='addproductcategory'),
    path('manageproductcategory/', manageproductcategory, name='manageproductcategory'),
    path('editproductcategory/<int:pctid>?', editproductcategory, name='editproductcategory'),
    path('delete_product_category/<int:pid>?', delete_product_category, name='delete_product_category'),

    path('addproducts/', addproducts, name='addproducts'),
    path('manageproducts/', manageproducts, name='manageproducts'),
    path('editproduct/<int:pid>?', editproduct, name='editproduct'),
    path('delete/<int:pid>?', delete_product, name='delete_product'),
    path('profile/<int:id>/', profile, name='profile'),
    path('changepassword/<int:id>/', changepassword, name='changepassword'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    path('page/', page, name='page'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
