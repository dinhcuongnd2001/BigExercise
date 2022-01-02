from django.contrib import admin
from .models import Review
# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ['id','user','product','rate','created_at']
#     readonly_fields =['created_at',]