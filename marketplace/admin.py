from django.contrib import admin

from marketplace.models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)

