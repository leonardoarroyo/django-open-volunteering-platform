# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20161118_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='can_be_done_remotely',
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=models.CharField(
                default='-',
                max_length=4000,
                verbose_name='Description'),
            preserve_default=False,
        ),
    ]
