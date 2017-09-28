# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_categoryfilter_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='catalogue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='catalogue.Catalogue'),
        ),
        migrations.AlterField(
            model_name='sectionfilter',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='catalogue.Section'),
        ),
    ]
