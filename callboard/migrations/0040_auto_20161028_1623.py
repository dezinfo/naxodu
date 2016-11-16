# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('callboard', '0039_auto_20161028_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeMap',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('attribute', models.ForeignKey(related_name='attribute', to='callboard.Attribute')),
                ('product', models.ForeignKey(to='callboard.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('vallue', models.CharField(max_length=50)),
                ('attribute', models.ForeignKey(to='callboard.Attribute')),
            ],
        ),
        migrations.AddField(
            model_name='attributemap',
            name='value',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='attribute', verbose_name='Значение аттрибута', auto_choose=True, to='callboard.AttributeValue', chained_model_field='attribute'),
        ),
    ]
