# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-08 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0006_auto_20171204_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='language',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Language'),
        ),
    ]