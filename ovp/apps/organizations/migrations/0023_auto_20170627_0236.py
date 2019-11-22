# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-27 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0022_auto_20170613_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.OneToOneField(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.GoogleAddress',
                verbose_name='address'),
        ),
    ]
