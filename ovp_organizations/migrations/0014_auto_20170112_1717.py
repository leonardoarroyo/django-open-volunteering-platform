# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-12 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0013_auto_20170112_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Organization'), (1, 'School'), (2, 'Company'), (3, 'Group of volunteers')], default=(0, 'Organization'), verbose_name='Type'),
        ),
    ]
