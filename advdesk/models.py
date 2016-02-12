#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from time import  time
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.


def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s/%s/%s_%s' % (instance.user.username,instance.good.id,str(time()).replace('.','_'),filename)

class Category(models.Model):
    name = models.CharField(verbose_name='Категория',max_length=150 , unique=True)
    description = models.TextField(verbose_name='Описание', null=True,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        managed=True

class SubCategory(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    name = models.CharField(verbose_name='Подкатегория',max_length=150)
    description = models.TextField(verbose_name='Описание', null=False,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        unique_together = ('category', 'name')
        managed = True

class Goods(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True, verbose_name='Подкатегория',blank=True
    )

    name = models.CharField(verbose_name='Заголовок',max_length=250)
    price = models.IntegerField(verbose_name='Цена', null=False,blank=True)
    description = models.TextField(verbose_name='Описание', null=False,blank=True)
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True,editable=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    attribute = models.CharField(max_length=10,blank=True)
    class Meta:
        managed=True

    def __str__(self):              # __unicode__ on Python 2
        return self.name




class GoodsImageGallery (models.Model):
    good = models.ForeignKey(Goods)
    file = models.FileField(upload_to=get_upload_file_name)
    user = models.ForeignKey(User)
    # creation_date = models.DateField('date published',auto_now_add=True)
    # is_main = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
       return (str(self.good)+' id '+str(self.good_id))

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
    attrname = models.ForeignKey(Attributes,verbose_name='Аттрибут',max_length=30)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.category)+'-'+str(self.subcategory)+'-'+str(self.attrname)

    class Meta:
        unique_together = ('category', 'subcategory','attrname')
        managed = True