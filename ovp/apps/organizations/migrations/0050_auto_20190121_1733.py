# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-01-21 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0049_merge_20181210_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='benefited_people',
            field=models.IntegerField(
                default=0),
        ),
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
