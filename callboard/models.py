#-*- coding: utf-8 -*-
import itertools
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from time import  time
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from django.conf import  settings
from PIL import Image
from pytils.translit import slugify
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib import admin
from ckeditor.fields import RichTextField
from userprofile.models import States,Cities
from django.contrib.postgres.fields import JSONField
from userprofile.models import States,Cities


# Create your models here.

CONDITION = (('New','Новый'),('Old','Б/У'))
CURR = (('UAH','Гривна'),('USD','Доллар'),('EUR','Евро'))
VALUE_TYPE = (('choice','Справочник'),('text','Текст'), ('number','Число'))

class GoodsManager(models.Manager):

    def only_active(self):

        return self.filter(is_active=True)


    def order_by(self):
        return  self.order_by('-order_date')



def get_upload_file_name(instance, filename):
    return 'uploaded_files/%s/%s/%s_%s' % (instance.user.username,instance.good.id,str(time()).replace('.','_'),filename)


class CurrencyRate(models.Model):
    currency = models.CharField(max_length=3)
    rate = models.FloatField()

class Attribute(models.Model):
    name = models.CharField(max_length=30)
    verbos_name = models.CharField(max_length=50)
    ordering = models.PositiveIntegerField(verbose_name="Сортировка", blank=True, null=True)
    attr_type = models.CharField(verbose_name="Тип поля",choices=VALUE_TYPE, max_length=15,default='text')
    required = models.BooleanField(default=False)
    filtering = models.BooleanField(default=False)
    key_words = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
       return str(self.name)



class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute)
    vallue = models.CharField(max_length=50)


    def __str__(self):              # __unicode__ on Python 2
       return str(self.vallue)



class AttributeValueOptions(admin.ModelAdmin):
    # define the raw_id_fields
    raw_id_fields = ('attribute')
    # define the related_lookup_fields
    related_lookup_fields = {
        'fk': ['attribute'],

    }


class Category(models.Model):
    name = models.CharField(verbose_name='Категория',max_length=60 , unique=True)
    description = models.TextField(verbose_name='Описание', null=True,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    slug = models.SlugField(max_length=60,blank=True)
    follow = models.ManyToManyField(User,blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


    def admin_name(self):              # __unicode__ on Python 2
         return self.name+' pk- '+str(self.pk)


    admin_name.short_description = 'Full name'


    class Meta:
        managed=True



    def count_products(self):

        return Goods.objects.only_active().filter(category=self.pk).count()

    def save(self,*args,**kwargs):


           self.slug = slugify(self.name)
           super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return  reverse('category', kwargs={'category': self.slug})

class SubCategory(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    name = models.CharField(verbose_name='Подкатегория',max_length=60)
    description = models.TextField(verbose_name='Описание', null=False,blank=True)
    image = models.ImageField(verbose_name='Изображение', null=True,blank=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    creation_date = models.DateTimeField('date published',auto_now_add=True)
    slug = models.SlugField(max_length=60,blank=True)
    follow = models.ManyToManyField(User,blank=True,related_name='sub_category')
    attributes = models.ManyToManyField(Attribute, verbose_name='Доступные аттрибуты', blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def admin_name(self):              # __unicode__ on Python 2
         return self.category.name+'\\'+self.name +' pk- '+ str(self.pk)


    admin_name.short_description = 'Full name'

    def count_products(self):

        return Goods.objects.only_active().filter(subcategory=self.pk).count()

    class Meta:
        unique_together = ('category', 'name')
        managed = True

    def save(self,*args,**kwargs):
        if not self.slug:
            # self.slug = slugify(self.name)
            self.slug = orig = slugify(self.name)

            for x in itertools.count(1):
                if not SubCategory.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)


        super(SubCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return  reverse('subcategory', kwargs={'category': self.category.slug, 'subcategory':self.slug})



class Type(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')
    subcategory = models.ForeignKey(SubCategory,verbose_name='Подкатегория',blank=True,related_name='type')
    name = models.CharField(verbose_name='Тип',max_length=60, unique=True)
    slug = models.SlugField(max_length=60,blank=True)
    attributes = models.ManyToManyField(Attribute, verbose_name='Доступные аттрибуты', blank=True)
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)

    def __str__(self):              # __unicode__ on Python 2
        return self.name



    def admin_name(self):              # __unicode__ on Python 2
         return self.category.name+'>'+self.subcategory.name+'>'+self.name


    admin_name.short_description = 'Full name'



class Goods(models.Model):
    category = models.ForeignKey(Category,verbose_name='Карегория')

    # subcategory = ChainedForeignKey(
    #     SubCategory,
    #     chained_field="category",
    #     chained_model_field="category",
    #     show_all=False,
    #     auto_choose=True, verbose_name='Подкатегория',blank=True
    # )

    subcategory = models.ForeignKey(SubCategory,verbose_name='Подкатегория',related_name='subcategory_set')

    # type = ChainedForeignKey(
    #     Type,
    #     chained_field="subcategory",
    #     chained_model_field="subcategory",
    #     show_all=False,
    #     auto_choose=True, verbose_name='Тип',blank=True
    # )

    types = models.ForeignKey(Type, verbose_name='Тип', null=True, related_name='type_set')
    name = models.CharField(verbose_name='Заголовок',max_length=250)
    price = models.PositiveIntegerField(verbose_name='Цена', null=False,blank=False)
    description = RichTextField(verbose_name='Описание', null=False,blank=False,config_name='good_ckeditor')
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='date_update',auto_now=True)
    user = models.ForeignKey(User,max_length=100,verbose_name='Пользователь', null=True)
    views = models.PositiveIntegerField(verbose_name='Просмотров',default=0)
    is_salles = models.BooleanField(verbose_name='Распродажа', default=False)
    salles_price = models.PositiveIntegerField(verbose_name='Цена распродажи',blank=True,default=0)
    # condition = models.CharField(verbose_name='Состояние',choices=CONDITION,max_length=15,blank=False)
    is_active = models.BooleanField(verbose_name='Доступно', default=True)
    # is_aukc = models.BooleanField(verbose_name='На аукционе', default=False)
    rate = models.PositiveIntegerField(verbose_name='Рейтинг',default=0,max_length=1)
    state = models.ForeignKey(States,verbose_name='Область',null=True,blank=True)
    city = models.ForeignKey(Cities,verbose_name='Город',null=True,blank=True)
    currency = models.CharField(choices=CURR, default='UAH', max_length=3)
    order_date = models.DateTimeField(verbose_name='Дата для сортировки', blank=True)
    attributes = JSONField(verbose_name='Аттрибуты',null=True)
    state = models.ForeignKey(States,verbose_name='Область', related_name='state_set',null=True)
    city = models.ForeignKey(Cities, verbose_name='Город',related_name='city_set', null=True)


    # city = ChainedForeignKey(
    #     Cities,
    #     chained_field="state",
    #     chained_model_field="state",
    #     show_all=False,
    #     auto_choose=False, verbose_name='Город',null=True
    # )
    objects = GoodsManager()

    @property
    def is_aukc(self):

        a =  self.auction_set.filter(product_id=self.pk).latest('end_date')

        if a.is_canceled == False:
            return True
        else:
            return False


    class Meta:
        managed=True



    def __str__(self):              # __unicode__ on Python 2
        return self.name+' id='+str(self.pk)


    def save(self,*args,**kwargs):



        try:
            self.state = self.user.userprofile_set.all().get().adress_state
            self.city = self.user.userprofile_set.all().get().adress_city
        except:
            pass

        if self.order_date is None:
           self.order_date=timezone.now()
        else:
            delta = timezone.now()-self.creation_date
            if delta.days >= 30:
                self.order_date=timezone.now()

        super(Goods, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return  reverse('advdetail', kwargs={'pk': self.pk})


    def ua_price(self):

       if self.is_salles:
        if self.currency != 'UAH':

            rate = CurrencyRate.objects.get(currency=self.currency).rate

            price = self.salles_price * rate
            old_price = self.price * rate
            if self.currency=='USD':
                cc = '$'
            else:
                cc = '&#8364;'

            return round(price), cc , round(old_price)
        else:
            return self.salles_price, 'грн', self.price
       else:
           if self.currency != 'UAH':

                rate = CurrencyRate.objects.get(currency=self.currency).rate

                price = self.price * rate

                if self.currency=='USD':
                    cc = '$'
                else:
                    cc = '&#8364;'

                return round(price), cc
           else:
              return self.price, 'грн'

    def order_count(self):

        oc =self.order_goods.filter(order__order_status__in=['Accept','New','Reject']).count()


        return oc

    # def actual_price(self):
    #     if (self.is_salles == True):
    #
    #         return self.salles_price
    #     else:
    #         return self.ua_price()[0]

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


class AttributeMap(models.Model):
      product_name = models.ForeignKey(Goods)
      attribute_name = models.ForeignKey(Attribute, related_name='attribute')
      attribute_value = ChainedForeignKey(
      AttributeValue,
      chained_field="attribute_name",
      chained_model_field="attribute",
      show_all=False,
      auto_choose=False, verbose_name='Значение аттрибута',blank=True, null=True)
      attribute_value_manual = models.CharField(max_length=150, blank=True)


      def value(self):
          if self.attribute_value is None:

              return self.attribute_value_manual
          else:
            return self.attribute_value

      def __str__(self):              # __unicode__ on Python 2
        return str(self.product_name.name+' '+self.attribute_name.name+' '+str(self.value()))




class CatType(models.Model):
    name = models.CharField(max_length=120);
    releted_sub = models.ManyToManyField(SubCategory)

    def __str__(self):              # __unicode__ on Python 2
       return str(self.name)





