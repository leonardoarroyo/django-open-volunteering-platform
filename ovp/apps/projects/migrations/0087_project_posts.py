# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-25 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_post'),
        ('projects', '0086_remove_project_commentaries'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='posts',
            field=models.ManyToManyField(
                to='core.Post',
                verbose_name='galleries'),
        ),
    ]
