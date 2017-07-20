# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-17 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0015_merge_20170112_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Organization'), (1, 'School'), (2, 'Company'), (3, 'Group of volunteers')], default=0, verbose_name='Type'),
        ),
    ]
