from django.contrib import admin

from shop.models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)

