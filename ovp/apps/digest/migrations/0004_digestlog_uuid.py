# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-03 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('digest', '0003_digestlogcontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='digestlog',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
