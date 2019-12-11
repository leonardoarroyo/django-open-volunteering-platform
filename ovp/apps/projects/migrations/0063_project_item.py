# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-15 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20180715_1412'),
        ('projects', '0062_auto_20180705_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='item',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='items.Item',
                verbose_name='item'),
        ),
    ]
