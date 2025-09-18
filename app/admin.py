from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(WebsiteAdmin)
admin.site.register(ProductCategory)
admin.site.register(Products)
admin.site.register(ContactInfo)
admin.site.register(AboutInfo)

