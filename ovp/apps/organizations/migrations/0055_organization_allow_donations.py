# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-20 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0054_auto_20190418_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='allow_donations',
            field=models.BooleanField(
                default=False,
                verbose_name='Allow donations'),
        ),
    ]
