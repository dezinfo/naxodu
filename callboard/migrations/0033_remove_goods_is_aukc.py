# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-04 09:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0032_goods_is_aukc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='is_aukc',
        ),
    ]