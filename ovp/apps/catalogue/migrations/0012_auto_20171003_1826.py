# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 18:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_auto_20171003_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections'},
        ),
    ]
