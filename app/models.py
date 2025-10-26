from django.db import models

# Create your models here.

class WebsiteAdmin(models.Model):
    username = models.CharField(max_length=191, unique=True)
    password = models.CharField(max_length=191)  # hashed password
    email = models.EmailField(unique=True, max_length=191)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class ProductCategory(models.Model):
    pctid=models.IntegerField(primary_key=True)
    pctname=models.CharField(max_length=191)
    pimage=models.ImageField(upload_to='media/productcategory/', blank=True, null=True)

    def __str__(self):
        return self.pctname
    
class Products(models.Model):
    pid=models.IntegerField(primary_key=True)
    pname=models.CharField(max_length=191)
    pctid=models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    pdesc=models.CharField(max_length=191)
    pprice=models.DecimalField(max_digits=10, decimal_places=2)
    pimage=models.ImageField(upload_to='media/products/', blank=True, null=True)
    pcreated=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pname
    
class ContactInfo(models.Model):
    c_address=models.CharField(max_length=191)
    c_email=models.EmailField(unique=True, max_length=191)
    c_phone=models.CharField(max_length=191)

class AboutInfo(models.Model):
    c_vision=models.CharField(max_length=191)
    c_mission=models.CharField(max_length=191)

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="media/products/multiple/")

    def __str__(self):
        return f"{self.product.pname} - Image"