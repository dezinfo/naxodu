# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-27 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0002_goods_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='is_salles',
            field=models.BooleanField(default=False, verbose_name='Распродажа'),
        ),
        migrations.AddField(
            model_name='goods',
            name='salles_price',
            field=models.IntegerField(blank=True, default=0, verbose_name='Цена распродажи'),
        ),
    ]
