# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-20 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_project_max_applies_from_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='dates',
        ),
        migrations.AddField(
            model_name='jobdate',
            name='job',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='dates',
                to='projects.Job'),
        ),
        migrations.AlterField(
            model_name='jobdate',
            name='name',
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                verbose_name='Label'),
        ),
    ]
