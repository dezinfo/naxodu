from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from _datetime import datetime
from callboard.models import Goods

ORDER_STATUS = (('Draft','Draft'),('New','New'),('Reject','Reject'),('Accept','Accept'))
FIELD_TYPE = (('Text','Text'),('Choice','Choice'),('Int','Int'))
# Create your models here.


class OrderItems(models.Model):
    order_id = models.PositiveIntegerField(verbose_name='order_id',default=0)
    good = models.ForeignKey(Goods,related_name='order_goods')
    qty = models.PositiveIntegerField(verbose_name='Кол-во',default=1)
    comment = models.CharField(verbose_name='Комментарий',max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.order_id)

class DelivertType(models.Model):
    name = models.CharField(verbose_name='Транспортная компания',max_length=60)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)

class DeliveryOption(models.Model):
     delivery_name = models.ForeignKey(DelivertType)
     option_name = models.CharField(verbose_name='Опция доставки',max_length=60)
     order = models.PositiveIntegerField(verbose_name='Порядок сортировки',default=0)
     field_type = models.CharField(verbose_name='', choices=FIELD_TYPE,default='Text', max_length=20)
     def __str__(self):              # __unicode__ on Python 2
        return str(self.delivery_name)


class Order(models.Model):
    buyer = models.ForeignKey(User,verbose_name='Покупатель',related_name='order_buyer')
    seller = models.ForeignKey(User,verbose_name='Продавец',related_name='order_seller')
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True,null=True)
    responce_date = models.DateTimeField(blank=True,null=True)
    order_status = models.CharField(choices=ORDER_STATUS,default='Draft',blank=True,max_length=20)
    buyer_fb = models.BooleanField(default=False)
    seller_fb = models.BooleanField(default=False)
    ordered_items = models.ManyToManyField(OrderItems)
    dilivery_adress = JSONField(null=True,blank=True)

    # пример сохранения адреса доставки dilivery_adress = JSONField()
    # dilivery_adress = {
    #     'del_type_id': 'id',
    #     'del_option_id': {'option_name': 'option_value'}}

    class Meta:

        managed = True




    def __str__(self):              # __unicode__ on Python 2
        return 'From '+self.buyer.username+' order_id '+str(self.pk)


    def save(self, *args, **kw):

        # status = self.objects.get(pk=self.pk).order_status

        if self.order_status != 'Draft':
            if self.order_status == 'New':
                self.ordered_date = datetime.now()
            elif self.order_status == 'Reject' or 'Accept':
                self.responce_date = datetime.now()


        super(Order, self).save(*args, **kw)




