# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_passwordrecoverytoken_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordrecoverytoken',
            name='used',
            field=models.DateTimeField(
                blank=True,
                default=None,
                null=True),
        ),
        migrations.AlterField(
            model_name='passwordrecoverytoken',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='users.User'),
        ),
    ]
