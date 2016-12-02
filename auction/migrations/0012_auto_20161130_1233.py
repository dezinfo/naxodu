# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0011_auto_20161114_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Аукцион закрыт'),
        ),
        migrations.AddField(
            model_name='auction',
            name='winner_notified',
            field=models.BooleanField(default=False, verbose_name='Победитель проинформирован'),
        ),
    ]