# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_auto_20161121_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiletable',
            name='user_image',
            field=models.ImageField(blank=True, default='/Users/korablevop/PycharmProjects/naxodu/static//images/avatar.jpeg', upload_to='', verbose_name='Аватар'),
        ),
    ]
