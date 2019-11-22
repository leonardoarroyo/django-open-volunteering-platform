# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-05 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0009_uploadeddocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadeddocument',
            name='extension',
            field=models.CharField(
                blank=True,
                max_length=5,
                null=True,
                verbose_name='Extension'),
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='size',
            field=models.IntegerField(
                blank=True,
                default=0,
                null=True,
                verbose_name='Size'),
        ),
    ]
