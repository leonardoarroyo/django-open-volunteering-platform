# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-01 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0092_project_flairs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='benefited_people',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Benefited people'),
        ),
    ]
