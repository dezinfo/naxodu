from django.db import models
from django.contrib.auth.models import User
from _datetime import datetime
from callboard.models import Goods

ORDER_STATUS = (('Draft','Draft'),('New','New'),('Reject','Reject'),('Accept','Accept'))
# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(User,verbose_name='Покупатель',related_name='order_buyer')
    seller = models.ForeignKey(User,verbose_name='Продавец',related_name='order_seller')
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True,null=True)
    responce_date = models.DateTimeField(blank=True,null=True)
    order_status = models.CharField(choices=ORDER_STATUS,default='Draft',blank=True,max_length=20)
    buyer_fb = models.BooleanField(default=False)
    seller_fb = models.BooleanField(default=False)


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

class OrderItems(models.Model):
    order = models.ForeignKey(Order)
    good = models.ForeignKey(Goods,related_name='order_item_goods')
    comment = models.CharField(verbose_name='Комментарий',max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.order)


