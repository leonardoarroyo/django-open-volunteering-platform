# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_users', '0004_passwordrecoverytoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordrecoverytoken',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
