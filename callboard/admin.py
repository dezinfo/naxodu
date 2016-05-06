from django.contrib import admin
from callboard.models import *

# Register your models here.


class SubTypeAdmin(admin.ModelAdmin):
  model = SubType
  list_display = ['admin_name',]

class SubCategoryAdmin(admin.ModelAdmin):
  model = SubCategory
  list_display = ['admin_name',]

admin.site.register(Category)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Goods)
admin.site.register(SubCategoryAttr)
admin.site.register(Attributes)
admin.site.register(GoodsImageGallery)
admin.site.register(Type)
admin.site.register(SubType,SubTypeAdmin)


