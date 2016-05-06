#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from time import  time
from smart_selects.db_fields import ChainedForeignKey
from django_hstore import hstore
from django.conf import  settings
from PIL import Image
from pytils.translit import slugify
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from tinymce.models import HTMLField


# Create your models here.

CONDITION = (('New','Новый'),('Old','Б/У'))

def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s/%s/%s_%s' % (instance.user.username,instance.good.id,str(time()).replace('.','_'),filename)

class Category(models.Model):
    name = models.CharField(verbose_name='Категория',max_length=60 , unique=True)
    description = models.TextField(verbose_name='Описание', null=True,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    slug = models.SlugField(max_length=60,blank=True)
    follow = models.ManyToManyField(User,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        managed=True

    def save(self,*args,**kwargs):


           self.slug = slugify(self.name)
           super(Category, self).save(*args, **kwargs)



class SubCategory(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    name = models.CharField(verbose_name='Подкатегория',max_length=60)
    description = models.TextField(verbose_name='Описание', null=False,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True)
    slug = models.SlugField(max_length=60,blank=True)
    follow = models.ManyToManyField(User,blank=True,related_name='sub_category')


    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def admin_name(self):              # __unicode__ on Python 2
         return self.category.name+'\\'+self.name


    admin_name.short_description = 'Full name'


    class Meta:
        unique_together = ('category', 'name')
        managed = True

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)



class Type(models.Model):

    name = models.CharField(verbose_name='Тип',max_length=60)
    slug = models.SlugField(max_length=60,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class SubType(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name='Подкатегория')
    type = models.ForeignKey(Type, related_name='type_set')
    type_name = models.CharField(verbose_name='Тип',max_length=60)
    slug = models.SlugField(max_length=60,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.type_name)
        super(SubType, self).save(*args, **kwargs)


    def __str__(self):              # __unicode__ on Python 2
        return self.type_name

    def admin_name(self):              # __unicode__ on Python 2
        return self.subcategory.category.name+'\\'+ self.subcategory.name+'\\'+self.type.name+'\\'+self.type_name


    admin_name.short_description = 'Full name'




class Goods(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True, verbose_name='Подкатегория',blank=True
    )
    subtype = ChainedForeignKey(
        SubType,
        chained_field="subcategory",
        chained_model_field="subcategory",
        show_all=False,
        auto_choose=True, verbose_name='Тип',blank=True
    )
    name = models.CharField(verbose_name='Заголовок',max_length=250)
    price = models.IntegerField(verbose_name='Цена', null=False,blank=False)
    description = HTMLField(verbose_name='Описание', null=False,blank=False)
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='date_update',auto_now=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    data = hstore.DictionaryField(verbose_name='Data',blank=True)
    objects = hstore.HStoreManager()
    views = models.IntegerField(verbose_name='Просмотров',default=0)
    is_salles = models.BooleanField(verbose_name='Распродажа', default=False)
    salles_price = models.IntegerField(verbose_name='Цена распродажи',blank=True,default=0)
    condition = models.CharField(verbose_name='Состояние',choices=CONDITION,max_length=15,blank=False)
    is_active = models.BooleanField(verbose_name='Доступно', default=True)

    class Meta:
        managed=True

    def __str__(self):              # __unicode__ on Python 2
        return self.name+' id='+str(self.pk)

    def order_count(self):

        oc =self.order_item_goods.filter(order__order_status__in=['Accept','New','Reject']).count()


        return oc

    def actual_price(self):
        if self.is_salles == True:
            return self.salles_price
        else:
            return self.price

    def sales_percent(self):
        if self.is_salles == True:
            return round(100-(self.salles_price*100/self.price))



    def get_image(self):

            photo = GoodsImageGallery.objects.filter(good=self.id)[:1]

            if len(photo)>0:

                image = photo.get().file
            else:
                image = settings.MEDIA_ROOT+'no_image.jpg'

            return image


class GoodsImageGallery (models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_file_name)
    user = models.ForeignKey(User)
    # creation_date = models.DateField('date published',auto_now_add=True)
    # is_main = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
       return str(self.good)

    def save(self,**kwargs):


           super(GoodsImageGallery, self).save()

           image = Image.open(self.file )
           image.save(self.file.path,quality=30,optimize=True)


@receiver(pre_delete, sender=GoodsImageGallery)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


class Attributes(models.Model):
    name = models.CharField(verbose_name='Имя аттрибута',max_length=50,unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class SubCategoryAttr(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True, verbose_name='Подкатегория',blank=True
    )
    attrname = models.ManyToManyField(Attributes,verbose_name='Аттрибуты',max_length=30,related_name='attrname_set',blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.category)+'-'+str(self.subcategory)

    class Meta:
        unique_together = ('category', 'subcategory')
        managed = True