# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0040_auto_20161028_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributemap',
            old_name='attribute',
            new_name='attribute_name',
        ),
        migrations.RenameField(
            model_name='attributemap',
            old_name='value',
            new_name='attribute_value',
        ),
        migrations.RenameField(
            model_name='attributemap',
            old_name='product',
            new_name='product_name',
        ),
    ]
