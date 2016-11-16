# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0044_attribute_verbos_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='verbos_name',
            field=models.CharField(max_length=50,null=True),
        ),
    ]
