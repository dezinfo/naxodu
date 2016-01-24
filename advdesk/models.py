#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Advertisement(models.Model):
    name = models.CharField(verbose_name='Объявление', max_length=300)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


