from django.contrib import admin
from callboard.models import *

# Register your models here.




class SubCategoryAdmin(admin.ModelAdmin):
  model = SubCategory
  list_display = ['admin_name',]

class CategoryAdmin(admin.ModelAdmin):
  model = Category
  list_display = ['admin_name',]


class TypeAdmin(admin.ModelAdmin):
  model = Type
  list_display = ['admin_name',]


admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Goods)
admin.site.register(CatType)

admin.site.register(GoodsImageGallery)
admin.site.register(Type)
admin.site.register(CurrencyRate)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(AttributeMap)






