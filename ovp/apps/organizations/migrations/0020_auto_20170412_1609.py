# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0019_auto_20170127_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='contact_email',
            field=models.EmailField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name='Responsible email'),
        ),
        migrations.AddField(
            model_name='organization',
            name='contact_name',
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name='Responsible name'),
        ),
        migrations.AddField(
            model_name='organization',
            name='contact_phone',
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name='Responsible phone'),
        ),
    ]
