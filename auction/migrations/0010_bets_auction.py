# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-13 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_auto_20161013_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='bets',
            name='auction',
            field=models.IntegerField(default=1, verbose_name='Идентификатор аукциона'),
            preserve_default=False,
        ),
    ]
