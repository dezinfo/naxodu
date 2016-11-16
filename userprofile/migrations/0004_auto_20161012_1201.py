# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-12 09:01
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20161006_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='adress_city',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='adress_state', chained_model_field='state', null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Cities', verbose_name='Город'),
        ),
    ]