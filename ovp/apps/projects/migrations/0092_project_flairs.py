# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-07 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_flair'),
        ('projects', '0091_apply_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='flairs',
            field=models.ManyToManyField(blank=True, related_name='projects', to='core.Flair', verbose_name='flairs'),
        ),
    ]
