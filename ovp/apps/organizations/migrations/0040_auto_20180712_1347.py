# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-12 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0039_auto_20180712_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='details',
            field=models.TextField(
                blank=True,
                default=None,
                max_length=3000,
                null=True,
                verbose_name='Details'),
        ),
    ]
