from django.contrib import admin
from .models import Category,SubCategory,Product,Brand,Slider,Contact,Order

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Slider)
admin.site.register(Contact)
admin.site.register(Order)
