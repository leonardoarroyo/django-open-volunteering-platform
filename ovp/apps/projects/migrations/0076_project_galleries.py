# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-28 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_gallery_owner'),
        ('projects', '0075_auto_20190121_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='galleries',
            field=models.ManyToManyField(to='gallery.Gallery', verbose_name='galleries'),
        ),
    ]