from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from app.models import *
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from classicelectricals import settings
from django.contrib.auth.decorators import login_required
from app.decorators import admin_login_required
from django.utils.text import slugify
import datetime
import re

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
    if not id:
        return redirect('adminlogin')
    
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

def category(request, pid, pctname):
    pcategory = get_object_or_404(ProductCategory, pctid=pid)
    PO = Products.objects.filter(pctid=pcategory)

    # Optional: if pctname in URL doesn’t match actual name, redirect to correct one
    correct_name = slugify(pcategory.pctname)
    if pctname != correct_name:
        return redirect('category', pid=pid, pctname=correct_name)

    return render(request, 'category.html', {'PO': PO, 'pcategory': pcategory})

def contact_email(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject", "No Subject")
        message = request.POST.get("message")

        #validations
        name_pattern= r'^[A-Za-z ]+$'
        email_pattern=r'^[a-z1-9]*[._%+-]?[a-z0-9]+@gmail[.]com$'
        mobile_pattern=r'^[6-9]\d{9}$'
        text_pattern = r'^[A-Za-z0-9\s.,!?@#$%^&*()_\-+=:;\'"<>/\\|`~]*$'

        if not re.match(name_pattern, name):
            messages.error(request, 'Invalid  Name! only alphabets and spaces allowed.')
            return redirect('contact')
        
        if not re.match(email_pattern, email):
            messages.error(request, 'Invalid  Email! Only Gmail addresses are allowed.')
            return redirect('contact')
        
        if not re.match(mobile_pattern, mobile):
            messages.error(request, 'Invalid mobile number! Must start with 6–9 and be 10 digits.')
            return redirect('contact')
        
        if not re.match(text_pattern, subject):
            messages.error(request, 'Invalid subject! Only alphabets, digits, and special characters are allowed.')
            return redirect('contact')
        
        if not re.match(text_pattern, message):
            messages.error(request, 'Invalid message! Only alphabets, digits, and special characters are allowed.')
            return redirect('contact')

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

        #validations
        name_pattern= r'^[A-Za-z ]+$'
        email_pattern=r'^[a-z1-9]*[._%+-]?[a-z0-9]+@gmail[.]com$'
        mobile_pattern=r'^[6-9]\d{9}$'
        text_pattern = r'^[A-Za-z0-9\s.,!?@#$%^&*()_\-+=:;\'"<>/\\|`~]*$'

        if not re.match(name_pattern, name):
            messages.error(request, 'Invalid  Name! only alphabets and spaces allowed.')
            return redirect('requestq')
        
        if not re.match(email_pattern, email):
            messages.error(request, 'Invalid  Email! Only Gmail addresses are allowed.')
            return redirect('requestq')
        
        if not re.match(mobile_pattern, mobile):
            messages.error(request, 'Invalid mobile number! Must start with 6–9 and be 10 digits.')
            return redirect('requestq')
        
        if not re.match(text_pattern, subject):
            messages.error(request, 'Invalid subject! Only alphabets, digits, and special characters are allowed.')
            return redirect('requestq')
        
        if not re.match(text_pattern, message):
            messages.error(request, 'Invalid message! Only alphabets, digits, and special characters are allowed.')
            return redirect('requestq')

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
    if not id:
        return redirect('adminlogin')
    admin = WebsiteAdmin.objects.get(id=aid)
    totaladmin = WebsiteAdmin.objects.count()
    totalcount=Products.objects.count()
    totalpcat=ProductCategory.objects.count()
    return render(request, 'admin/dashboard.html', {'admin': admin, 'total':totalcount, 'totala':totaladmin, 'totalpcat':totalpcat})

@admin_login_required
def profile(request,id):
    aid = request.session.get('id')
    if not id:
        return redirect('adminlogin')
    try:
        admin = WebsiteAdmin.objects.get(id=aid)

        if request.method == 'POST':
            email = request.POST.get('email')

            email_pattern=r'^[a-z1-9]*[._%+-]?[a-z0-9]+@gmail[.]com$'

            if not re.match(email_pattern, email):
                messages.error(request, 'Invalid  Email! Only Gmail addresses are allowed.')
                return redirect('profile', id=admin.id)

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
    if not id:
        return redirect('adminlogin')
    
    admin=WebsiteAdmin.objects.get(id=aid)

    if request.method=='POST':
        npw=request.POST['npw']

        # -------- PASSWORD VALIDATION --------
        # Must contain: 1 uppercase, 1 digit, 1 special char, and at least 8 chars
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.fullmatch(pattern, npw or ''):
            messages.error(
                request,
                'Invalid Password: Must be at least 8 characters long\n'
                '''At least one uppercase letter \n 
                one digit \n  
                one special character.'''
            )
            return redirect('changepassword', id=admin.id)
        
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



######################### Products categories#########################################
def addproductcategory(request):
    id = request.session.get('id')
    if not id:
        return redirect('adminlogin')
    
    admin = WebsiteAdmin.objects.get(id=id)
    if request.method=='POST':
        pctid=request.POST.get('pctid')
        pctname=request.POST.get('pctname')
        pctimage=request.FILES.get('pctimage')

        #validations
        if not re.fullmatch(r'\d+', pctid or ''):
            messages.error(request, 'Invalid ID: Only digits are allowed.')
            return redirect('addproductcategory')
        
        if not re.fullmatch(r'[A-Za-z0-9 ]+', pctname or ''):
            messages.error(request, 'Invalid Name: Only letters, digits, and spaces are allowed.')
            return redirect('addproductcategory')
        
        if pctimage:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            file_ext = pctimage.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                messages.error(request, 'Invalid Image Format: Only JPG, JPEG, or PNG allowed.')
                return redirect('addproductcategory')
        else:
            messages.error(request, 'Please upload an image file.')
            return redirect('addproductcategory')

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
    if not id:
        return redirect('adminlogin')
    
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
    if not id:
        return redirect('adminlogin')
    
    admin = WebsiteAdmin.objects.get(id=id)

    # get the category by pctid
    category = ProductCategory.objects.get(pctid=pctid)

    if request.method == 'POST':
        pctname = request.POST.get('product_category_name')
        pctimage = request.FILES.get('product_cat_image')

        #validations
        if not re.fullmatch(r'[A-Za-z0-9 ]+', pctname or ''):
            messages.error(request, 'Invalid Name: Only letters, digits, and spaces are allowed.')
            return redirect('editproductcategory', pctid=pctid)
        
        if pctimage:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            file_ext = pctimage.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                messages.error(request, 'Invalid Image Format: Only JPG, JPEG, or PNG allowed.')
                return redirect('editproductcategory', pctid=pctid)
        else:
            messages.error(request, 'Please upload an image file.')
            return redirect('editproductcategory', pctid=pctid)

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
    if not id:
        return redirect('adminlogin')
    
    admin=WebsiteAdmin.objects.get(id=id)
    product_cat=ProductCategory.objects.get(pctid=pid)
    product_cat.delete()
    return redirect('manageproductcategory')
######################### Products #########################################

def addproducts(request):
    id = request.session.get('id')
    if not id:
        return redirect('adminlogin')
    
    admin = WebsiteAdmin.objects.get(id=id)
    PCO = ProductCategory.objects.all()

    if request.method == 'POST':
        pid = request.POST.get('product_id')
        pname = request.POST.get('product_name')
        pctname = request.POST.get('product_category')
        pimage = request.FILES.get('product_image')  # main image
        pdesc = request.POST.get('product_description')
        extra_images = request.FILES.getlist('extra_images')  # multiple images

        # -------- VALIDATIONS --------
        # 1️⃣ Product ID - only digits
        if not re.fullmatch(r'\d+', pid or ''):
            messages.error(request, 'Invalid Product ID: Only digits are allowed.')
            return redirect('addproducts')

        # 2️⃣ Product Name - only letters, numbers, and spaces
        if not re.fullmatch(r'[A-Za-z0-9 ]+', pname or ''):
            messages.error(request, 'Invalid Product Name: Only letters, digits, and spaces are allowed.')
            return redirect('addproducts')

        # 3️⃣ Category validation (must exist)
        try:
            PCTO = ProductCategory.objects.get(pctid=pctname)
        except ProductCategory.DoesNotExist:
            messages.error(request, 'Invalid Category selected.')
            return redirect('addproducts')

        # 4️⃣ Main image validation
        if pimage:
            allowed_ext = ['jpg', 'jpeg', 'png']
            file_ext = pimage.name.split('.')[-1].lower()
            if file_ext not in allowed_ext:
                messages.error(request, 'Invalid Main Image: Only JPG, JPEG, PNG allowed.')
                return redirect('addproducts')
        else:
            messages.error(request, 'Please upload a main product image.')
            return redirect('addproducts')


        # 6️⃣ Description - must not be empty and max 500 chars (you can adjust)
        if not pdesc or len(pdesc.strip()) < 5:
            messages.error(request, 'Invalid Description: Minimum 5 characters required.')
            return redirect('addproducts')

        # 7️⃣ Extra images validation
        for img in extra_images:
            ext = img.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                messages.error(request, f'Invalid Extra Image "{img.name}": Only JPG, JPEG, PNG allowed.')
                return redirect('addproducts')

        try:
            # validate category safely
            PCTO = ProductCategory.objects.get(pctid=pctname)

            # create the product
            product = Products.objects.create(
                pid=pid,
                pname=pname,
                pctid=PCTO,
                pimage=pimage,  # main image
                pdesc=pdesc
            )

            # save multiple extra images
            for img in extra_images:
                ProductImage.objects.create(product=product, image=img)

            # ✅ success message
            messages.success(request, '✅ Product added successfully!')
            return redirect('addproducts')

        except ProductCategory.DoesNotExist:
            messages.error(request, '⚠️ Selected category does not exist.')
        except Exception as e:
            print(e)
            messages.error(request, f'⚠️ Something went wrong: {e}')

    return render(request, 'admin/addproduct.html', {'admin': admin, 'PCO': PCO})

def manageproducts(request):
    id = request.session.get('id')
    if not id:
        return redirect('adminlogin')
    
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
    if not id:
        return redirect('adminlogin')
    
    admin = WebsiteAdmin.objects.get(id=id)
    PDO = Products.objects.get(pid=pid)
    PCO = ProductCategory.objects.all()

    if request.method == 'POST':
        pname = request.POST.get('product_name')
        pctname = request.POST.get('product_category')
        PCTO = ProductCategory.objects.get(pctid=pctname)
        pimage = request.FILES.get('product_image')
        pdesc = request.POST.get('product_description')
        extra_images = request.FILES.getlist('extra_images')  

        # -------- VALIDATIONS --------
        # 2️⃣ Product Name - only letters, numbers, and spaces
        if not re.fullmatch(r'[A-Za-z0-9 ]+', pname or ''):
            messages.error(request, 'Invalid Product Name: Only letters, digits, and spaces are allowed.')
            return redirect('editproduct', pid=pid)

        # 3️⃣ Category validation (must exist)
        try:
            PCTO = ProductCategory.objects.get(pctid=pctname)
        except ProductCategory.DoesNotExist:
            messages.error(request, 'Invalid Category selected.')
            return redirect('editproduct', pid=pid)

        # 4️⃣ Main image validation
        if pimage:
            allowed_ext = ['jpg', 'jpeg', 'png']
            file_ext = pimage.name.split('.')[-1].lower()
            if file_ext not in allowed_ext:
                messages.error(request, 'Invalid Main Image: Only JPG, JPEG, PNG allowed.')
                return redirect('editproduct', pid=pid)
        else:
            messages.error(request, 'Please upload a main product image.')
            return redirect('editproduct', pid=pid)


        # 6️⃣ Description - must not be empty and max 500 chars (you can adjust)
        if not pdesc or len(pdesc.strip()) < 5:
            messages.error(request, 'Invalid Description: Minimum 5 characters required.')
            return redirect('editproduct', pid=pid)

        # 7️⃣ Extra images validation
        for img in extra_images:
            ext = img.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                messages.error(request, f'Invalid Extra Image "{img.name}": Only JPG, JPEG, PNG allowed.')
                return redirect('editproduct', pid=pid)

        try:
            # update product fields
            PDO.pname = pname
            PDO.pctid = PCTO
            if pimage:  # update only if a new main image is uploaded
                PDO.pimage = pimage
            PDO.pdesc = pdesc
            PDO.save()

            # ✅ Save new extra images
            if extra_images:
                for img in extra_images:
                    ProductImage.objects.create(product=PDO, image=img)

            messages.success(request, '✅ Product updated successfully!')
            return redirect('editproduct', pid=pid)

        except Exception as e:
            print("Error while updating product:", e)
            messages.error(request, '⚠️ Something went wrong while updating product.')
            return redirect('editproduct', pid=pid)

    return render(request, 'admin/editproduct.html', {
        'admin': admin,
        'PCO': PCO,
        'PDO': PDO
    })



def delete_product(request, pid):
    id=request.session.get('id')
    if not id:
        return redirect('adminlogin')
    
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