# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-07 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_flair'),
        ('users', '0056_userprofile_has_done_volunteer_work_before'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='flairs',
            field=models.ManyToManyField(
                blank=True,
                related_name='users',
                to='core.Flair',
                verbose_name='flairs'),
        ),
    ]
