# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 20:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0007_channelsetting'),
        ('core', '0023_auto_20171204_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='channel',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='availability_channel', to='channels.Channel'),
            preserve_default=False,
        ),
    ]
