# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0053_auto_20181022_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.CharField(
                blank=True,
                max_length=300,
                null=True,
                verbose_name='Department'),
        ),
    ]
