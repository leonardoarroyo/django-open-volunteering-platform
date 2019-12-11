# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-02 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_project_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ManyToManyField(
                to='projects.Category',
                verbose_name='category'),
        ),
    ]
