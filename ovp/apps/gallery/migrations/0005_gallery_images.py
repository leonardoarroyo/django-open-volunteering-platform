# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-03-08 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0016_auto_20190121_1733'),
        ('gallery', '0004_gallery_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='images',
            field=models.ManyToManyField(to='uploads.UploadedImage'),
        ),
    ]
