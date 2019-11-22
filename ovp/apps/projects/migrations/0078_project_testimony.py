# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-13 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0077_project_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='testimony',
            field=models.TextField(
                blank=True,
                max_length=3000,
                null=True,
                verbose_name='testimony'),
        ),
    ]
