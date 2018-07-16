# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-15 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdocument',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AddField(
            model_name='itemdocument',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Deleted date'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Deleted date'),
        ),
    ]
