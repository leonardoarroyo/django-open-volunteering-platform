# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-17 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0054_auto_20190418_2028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([]),
        ),
    ]