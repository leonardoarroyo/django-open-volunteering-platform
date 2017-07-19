# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 18:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20170222_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_userprofile_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
