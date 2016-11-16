# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0042_subcategory_attributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='data',
        ),
        migrations.AlterField(
            model_name='attributemap',
            name='attribute_value',
            field=smart_selects.db_fields.ChainedForeignKey(to='callboard.AttributeValue', verbose_name='Значение аттрибута', auto_choose=True, chained_field='attribute_name', chained_model_field='attribute', blank=True),
        ),
    ]
