# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-25 20:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0085_auto_20190617_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='commentaries',
        ),
    ]
