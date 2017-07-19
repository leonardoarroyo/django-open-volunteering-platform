# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_user_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='public',
            field=models.BooleanField(default=True, verbose_name='Public Profile'),
        ),
    ]
