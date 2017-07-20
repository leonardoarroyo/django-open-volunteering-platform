# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-09 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_uploadedimage_uuid'),
        ('organizations', '0010_auto_20161208_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='uploads.UploadedImage'),
        ),
    ]
