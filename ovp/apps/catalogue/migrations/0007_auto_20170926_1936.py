# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_categoryfilter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionfilter',
            name='content_type',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.ContentType'),
        ),
    ]
