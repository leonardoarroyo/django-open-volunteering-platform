# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-11-26 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0072_remove_apply_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='benefited_people',
            field=models.IntegerField(default=0),
        ),
    ]
