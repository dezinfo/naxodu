# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0047_attribute_ordering'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='condition',
        ),
    ]
