# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-06 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0026_auto_20190806_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
        ),
    ]
