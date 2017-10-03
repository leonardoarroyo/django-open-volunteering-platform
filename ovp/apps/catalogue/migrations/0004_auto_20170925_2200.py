# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('catalogue', '0003_sectionfilter_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionfilter',
            name='content_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sectionfilter',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]