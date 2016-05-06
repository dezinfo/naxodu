from django.db import models
from django.contrib.auth.models import User
from callboard.models import Goods

# Create your models here.

class Auctions(models.Model):
    lot = models.ForeignKey(Goods, verbose_name='Лот')
    start_price = models.IntegerField(verbose_name='Начальная цена')
    price_range = models.IntegerField(verbose_name='Мин шаг цены')
    extra_price = models.IntegerField(verbose_name='Экспрес продажа')
    start_date = models.DateTimeField(verbose_name='Дата начала аукциона')
    end_date = models.DateTimeField(verbose_name='Дата завершения аукциона')
    is_active = models.BooleanField(verbose_name='Активно')
    creation_date = models.DateTimeField('date published',auto_now_add=True)
    update_date = models.DateTimeField('date update',auto_now=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.lot.name