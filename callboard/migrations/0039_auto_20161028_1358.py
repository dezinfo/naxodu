# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0038_currencyrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('releted_sub', models.ManyToManyField(to='callboard.SubCategory')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='subcategoryattr',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='subcategoryattr',
            name='attrname',
        ),
        migrations.RemoveField(
            model_name='subcategoryattr',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subcategoryattr',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Attributes',
        ),
        migrations.DeleteModel(
            name='SubCategoryAttr',
        ),
    ]
