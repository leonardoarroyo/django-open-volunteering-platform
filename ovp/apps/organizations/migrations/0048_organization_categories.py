# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-11 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0070_auto_20181106_1540'),
        ('organizations', '0047_auto_20181106_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='categories',
            field=models.ManyToManyField(blank=True, to='projects.Category', verbose_name='categories'),
        ),
    ]
