# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0043_auto_20161103_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='verbos_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
