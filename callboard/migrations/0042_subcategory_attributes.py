# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0041_auto_20161028_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='attributes',
            field=models.ManyToManyField(blank=True, verbose_name='Доступные аттрибуты', to='callboard.Attribute'),
        ),
    ]
