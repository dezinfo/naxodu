#-*- coding: utf-8 -*-
from django.urls import reverse
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

from callboard.models import Goods


# Create your models here.

class Bets(models.Model):
    auction = models.IntegerField(verbose_name='Идентификатор аукциона')
    user = models.ForeignKey(User, related_name="user_bet")
    bet = models.IntegerField(verbose_name='Ставка')
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='date_update',auto_now=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.user.username + ' аукцион ' +str(self.auction) + ' ставка ' +str(self.bet)

class Auction(models.Model):
    product = models.ForeignKey(Goods)
    description = RichTextUploadingField(verbose_name='Описание')
    start_price = models.PositiveIntegerField(verbose_name='Начальная цена')
    end_price = models.PositiveIntegerField(verbose_name='Экспресс цена',blank=True,null=True )
    min_price_step = models.PositiveIntegerField(verbose_name='Минимальный шаг цены')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата завершения')
    creation_date = models.DateTimeField(verbose_name='date published',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='date_update',auto_now=True)
    winner_bet = models.ManyToManyField(Bets, related_name='winner_bets',null=True,blank=True)
    # winner = models.ForeignKey(User, related_name='who_winn', null=True, )
    # is_canceled = models.BooleanField(verbose_name='Аукцион завершен', default=False)
    #
    is_closed  = models.BooleanField(verbose_name='Аукцион закрыт', default=False)
    winner_notified  = models.BooleanField(verbose_name='Победитель проинформирован', default=False)

    def __str__(self):              # __unicode__ on Python 2



        return self.product.name



    @property
    def is_canceled(self):
        summ = 0
        b = self.winner_bet.aggregate(Max('bet'))['bet__max']
        if b is not None and self.end_price > 0:

            summ = self.end_price - (b)
        else:
            summ = self.start_price
        if (self.end_date <= timezone.now() or summ <= 0):
            return True
        else:
            return False



    def current_price(self):
        try:
            b = self.winner_bet.aggregate(Max('bet'))
            if b['bet__max'] is None:
                b = 0;
                bet = self.start_price;
            else:
                bet = b['bet__max']

        except:
            bet = 0



        # cp = self.start_price+bet

        return bet


    def bets(self):
        s = self.winner_bet.count()
        if s > 0:
            return s
        else:
            return 0



    def get_absolute_url(self):
        return  reverse('auction', kwargs={'auct_id': self.pk})
