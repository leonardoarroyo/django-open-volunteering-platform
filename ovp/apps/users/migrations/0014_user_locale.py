# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20170208_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='locale',
            field=models.CharField(blank=True, default='en', max_length=8, verbose_name='Locale'),
        ),
    ]
