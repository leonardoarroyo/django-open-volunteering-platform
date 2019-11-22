# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-06 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0069_merge_20181105_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='address',
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.GoogleAddress',
                verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.FloatField(
                choices=[
                    (1,
                     'Normal'),
                    (2,
                     'Donation')],
                default=1,
                max_length=10,
                verbose_name='Project Type'),
        ),
    ]
