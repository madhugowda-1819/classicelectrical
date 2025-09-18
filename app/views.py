from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from app.models import *
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from classicelectricals import settings
from django.contrib.auth.decorators import login_required
from app.decorators import admin_login_required
import datetime
# Create your views here.
def index(request):
    return render(request, 'index.html')

def product(request):
    category=ProductCategory.objects.annotate(total_products=Count('products'))
    return render(request, 'products.html',{'category':category})

def about(request):
    about_info=AboutInfo.objects.last()
    return render(request, 'about.html', {'about_info':about_info})

def contact(request):
    ccontact=ContactInfo.objects.last()
    return render(request, 'contact.html', {'ccontact':ccontact})

def requestq(request):
    return render(request, 'request.html')

def page(request):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)

    contactin, created_c = ContactInfo.objects.get_or_create(pk=1)
    aboutin, created_a = AboutInfo.objects.get_or_create(pk=1)

    if request.method == 'POST':
        if 'save_contact' in request.POST:  # contact form submit
            contactin.c_address = request.POST.get('address')
            contactin.c_email = request.POST.get('email')
            contactin.c_phone = request.POST.get('phone')
            contactin.save()
            messages.success(request, '✅ Contact information updated successfully!')
            return redirect('page')

        elif 'save_about' in request.POST:  # about form submit
            aboutin.c_vision = request.POST.get('Vission')
            aboutin.c_mission = request.POST.get('Mission')
            aboutin.save()
            messages.success(request, '✅ About information updated successfully!')
            return redirect('page')
        
    return render(request, 'admin/page.html', {
            'contact': contactin,
            'about': aboutin,
            'admin': admin,
        })

def allcategories(request):
    category=ProductCategory.objects.annotate(total_products=Count('products'))
    return render(request, 'allcategories.html', {'category':category})

def category(request, pid):
    pcategory=ProductCategory.objects.get(pctid=pid)
    PO=Products.objects.filter(pctid=pcategory)
    return render(request, 'category.html', {'PO':PO, 'pcategory':pcategory})

def minivisioncameras(request):
    pcategory=ProductCategory.objects.get(pctname='Machine Vision Cameras')
    PO=Products.objects.filter(pctid=pcategory)
    return render(request, 'minivisioncameras.html', {'PO':PO})

def contact_email(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject", "No Subject")
        message = request.POST.get("message")

        full_message = f"""
        Name: {name}
        Email: {email}
        Mobile: {mobile}
        Subject: {subject}
        Message: {message}
        """

        try:
            send_mail(subject, full_message, settings.EMAIL_HOST_USER, [settings.EMAIL_COMPANY], fail_silently=False)
            messages.success(request, "Your mail has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email")

        return redirect("contact")

    return render(request, "contact.html")

def request_email(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject", "No Subject")
        message = request.POST.get("message")

        full_message = f"""
        Name: {name}
        Email: {email}
        Mobile: {mobile}
        Subject: {subject}
        Message: {message}
        """

        try:
            send_mail(subject, full_message, settings.EMAIL_HOST_USER, [settings.EMAIL_COMPANY], fail_silently=False)
            messages.success(request, "Your mail has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email")

        return redirect("requestq")

    return render(request, "request.html")


@admin_login_required
def admin_dashboard(request):
    aid = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=aid)
    totaladmin = WebsiteAdmin.objects.count()
    totalcount=Products.objects.count()
    totalpcat=ProductCategory.objects.count()
    return render(request, 'admin/dashboard.html', {'admin': admin, 'total':totalcount, 'totala':totaladmin, 'totalpcat':totalpcat})

@admin_login_required
def profile(request,id):
    aid = request.session.get('id')
    try:
        admin = WebsiteAdmin.objects.get(id=aid)

        if request.method == 'POST':
            email = request.POST.get('email')
            admin.email = email
            admin.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', id=admin.id)

        return render(request, 'admin/profile.html', {'admin': admin})
    except WebsiteAdmin.DoesNotExist:
        messages.error(request, "Admin not found.")
        return redirect('adminlogin')

@admin_login_required
def changepassword(request, id):
    aid=request.session.get('id')
    admin=WebsiteAdmin.objects.get(id=aid)

    if request.method=='POST':
        npw=request.POST['npw']
        admin.password=make_password(npw)
        admin.save()
        messages.success(request, 'Password Changed Successfully.')
        return redirect('changepassword', id=admin.id)
    
    return render(request, 'admin/changepassword.html', {'admin': admin})


#admin login code
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = WebsiteAdmin.objects.get(username=username)
            if check_password(password, admin.password):
                request.session['id'] = admin.id
                return redirect('admin_dashboard')
            else:
                return render(request, 'admin/adminlogin.html', {'error': 'Invalid Username or Password'})
        except WebsiteAdmin.DoesNotExist:
            return render(request, 'admin/adminlogin.html', {'error': 'Invalid username'})
    
    return render(request, 'admin/adminlogin.html')

@admin_login_required
def admin_logout(request):
    request.session.flush()
    return redirect('adminlogin')


class SessionIdleTimeout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('id'):  # your admin session key
            now = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed = (now - datetime.datetime.fromisoformat(last_activity)).total_seconds()
                if elapsed > settings.SESSION_COOKIE_AGE:
                    request.session.flush()  # logout admin
                    return redirect('adminlogin')  # your login page url name

            request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response

######################### Products categories#########################################
def addproductcategory(request):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)
    if request.method=='POST':
        pctid=request.POST.get('pctid')
        pctname=request.POST.get('pctname')
        pctimage=request.FILES.get('pctimage')

        try:
            ProductCategory.objects.create(pctid=pctid, pctname=pctname, pimage=pctimage)
            messages.success(request, 'Product category Added Successfully')
            return redirect('addproductcategory')

        except:
            messages.error(request, 'Something Wrong')
            return redirect('addproductcategory')


    return render(request, 'admin/addcategory.html', {'admin':admin})

def manageproductcategory(request):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)
    
    search_query = request.GET.get('search', '')
    product_category_list = ProductCategory.objects.all().order_by('pctid')

    if search_query:
        product_category_list = product_category_list.filter(pctname__icontains=search_query)

    paginator = Paginator(product_category_list, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    PDO = paginator.get_page(page_number)

    return render(request, 'admin/managecategory.html', {'admin': admin,'PDO': PDO,'search_query': search_query})

def editproductcategory(request, pctid):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)

    # get the category by pctid
    category = ProductCategory.objects.get(pctid=pctid)

    if request.method == 'POST':
        pctname = request.POST.get('product_category_name')
        pctimage = request.FILES.get('product_cat_image')

        try:
            category.pctname = pctname
            category.pimage = pctimage

            category.save()
            messages.success(request, '✅ Product category updated successfully!')
            return redirect('editproductcategory', pctid=pctid)

        except Exception as e:
            print(e)
            messages.error(request, '⚠️ Something went wrong while updating the category.')
            return redirect('editcategory', pctid=pctid)

    return render(request, 'admin/editcategory.html', {'admin': admin, 'category': category, })


def delete_product_category(request, pid):
    id=request.session.get('id')
    admin=WebsiteAdmin.objects.get(id=id)
    product_cat=ProductCategory.objects.get(pctid=pid)
    product_cat.delete()
    return redirect('manageproductcategory')
######################### Products #########################################

def addproducts(request):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)
    PCO = ProductCategory.objects.all()

    if request.method == 'POST':
        pid = request.POST.get('product_id')
        pname = request.POST.get('product_name')
        pctname = request.POST.get('product_category')
        pimage = request.FILES.get('product_image')
        pprice = request.POST.get('product_price')
        pdesc = request.POST.get('product_description')

        try:
            # validate category safely
            PCTO = ProductCategory.objects.get(pctid=pctname)

            # create the product
            Products.objects.create(
                pid=pid,
                pname=pname,
                pctid=PCTO,
                pimage=pimage,
                pprice=pprice,
                pdesc=pdesc
            )

            # ✅ success message
            messages.success(request, '✅ Product added successfully!')
            return redirect('addproducts')

        except ProductCategory.DoesNotExist:
            messages.error(request, '⚠️ Selected category does not exist.')
        except Exception as e:
            print(e)
            messages.error(request, '⚠️ Something went wrong while adding product.')

    return render(request, 'admin/addproduct.html', {'admin': admin, 'PCO': PCO})


def manageproducts(request):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)
    
    search_query = request.GET.get('search', '')
    product_list = Products.objects.all().order_by('pid')

    if search_query:
        product_list = product_list.filter(pname__icontains=search_query)

    paginator = Paginator(product_list, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    PDO = paginator.get_page(page_number)

    return render(request, 'admin/manageproducts.html', {'admin': admin,'PDO': PDO,'search_query': search_query})

def editproduct(request, pid):
    id = request.session.get('id')
    admin = WebsiteAdmin.objects.get(id=id)
    PDO = Products.objects.get(pid=pid)
    PCO = ProductCategory.objects.all()

    if request.method == 'POST':
        pname = request.POST.get('product_name')
        pctname = request.POST.get('product_category')
        PCTO = ProductCategory.objects.get(pctid=pctname)
        pimage = request.FILES.get('product_image')
        pprice = request.POST.get('product_price')
        pdesc = request.POST.get('product_description')

        try:
            # update fields
            PDO.pname = pname
            PDO.pctid = PCTO
            if pimage:  # update only if a new file is uploaded
                PDO.pimage = pimage
            PDO.pprice = pprice
            PDO.pdesc = pdesc

            PDO.save()
            # ✅ Success message only if save passes
            messages.success(request, '✅ Product updated successfully!')
            return redirect('editproduct', pid=pid)

        except Exception as e:
            print(e)
            # ⚠️ Error message only if something goes wrong
            messages.error(request, '⚠️ Something went wrong while updating product.')
            return redirect('editproduct', pid=pid)

    return render(request, 'admin/editproduct.html', {'admin': admin, 'PCO': PCO, 'PDO': PDO})



def delete_product(request, pid):
    id=request.session.get('id')
    admin=WebsiteAdmin.objects.get(id=id)
    product=Products.objects.get(pid=pid)
    product.delete()
    return redirect('manageproducts')

# ################################ Conatct Info ###################################
# def contactinfo(request):
#     id = request.session.get('id')
#     admin = WebsiteAdmin.objects.get(id=id)

#     # get first or create if none
#     contactin, created = ContactInfo.objects.get_or_create(pk=1)  

#     if request.method == 'POST':
#         contactin.c_address = request.POST.get('address')
#         contactin.c_email = request.POST.get('email')
#         contactin.c_phone = request.POST.get('phone')
#         contactin.save()
#         # optional success message
#         messages.success(request, '✅ Contact information updated successfully!')
#         return redirect('contactinfo')  # refresh page after save

#     return render(request, 'admin/contactinfo.html', {'contact': contactin, 'admin':admin})


# def aboutinfo(request):
#     id = request.session.get('id')
#     admin = WebsiteAdmin.objects.get(id=id)

#     # get first or create if none
#     aboutin, created = AboutInfo.objects.get_or_create(pk=1)  

#     if request.method == 'POST':
#         aboutin.c_vision = request.POST.get('Vission')
#         aboutin.c_mission = request.POST.get('Mission')
#         aboutin.save()
#         # optional success message
#         messages.success(request, '✅ About information updated successfully!')
#         return redirect('aboutinfo')  # refresh page after save

#     return render(request, 'admin/aboutinfo.html', {'about': aboutin, 'admin':admin})