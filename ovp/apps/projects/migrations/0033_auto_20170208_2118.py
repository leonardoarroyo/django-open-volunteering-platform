# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20170206_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='email',
            field=models.CharField(blank=True, max_length=190, null=True, verbose_name='email'),
        ),
    ]