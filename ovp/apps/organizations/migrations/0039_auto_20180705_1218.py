# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-05 15:18
from __future__ import unicode_literals

from django.db import migrations, models
import ovp.apps.organizations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0038_auto_20180504_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='document',
            field=models.CharField(
                blank=True,
                max_length=18,
                null=True,
                unique=True,
                validators=[
                    ovp.apps.organizations.validators.validate_CNPJ],
                verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='verified',
            field=models.BooleanField(
                default=False,
                verbose_name='Verified'),
        ),
    ]
