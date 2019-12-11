# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-06 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_user_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='has_done_volunteer_work_before',
            field=models.NullBooleanField(
                default=None,
                verbose_name='Has done volunteer work before'),
        ),
    ]
