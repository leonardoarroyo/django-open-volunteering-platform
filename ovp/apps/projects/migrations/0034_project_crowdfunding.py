# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_auto_20170208_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='crowdfunding',
            field=models.BooleanField(
                default=False,
                verbose_name='Crowdfunding'),
        ),
    ]
