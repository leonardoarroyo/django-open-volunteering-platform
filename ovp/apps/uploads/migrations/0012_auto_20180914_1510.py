# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-14 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django_resized.forms
import ovp.apps.uploads.models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0011_uploadedimage_absolute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='image',
            field=models.ImageField(
                max_length=300,
                upload_to=ovp.apps.uploads.models.ImageName(),
                verbose_name='Image 350x260'),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='image_large',
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                default=None,
                force_format=None,
                keep_meta=True,
                max_length=300,
                null=True,
                quality=0,
                size=[
                    1260,
                    936],
                upload_to=ovp.apps.uploads.models.ImageName('-large')),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='image_medium',
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                default=None,
                force_format=None,
                keep_meta=True,
                max_length=300,
                null=True,
                quality=0,
                size=[
                    420,
                    312],
                upload_to=ovp.apps.uploads.models.ImageName('-medium')),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='image_small',
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                default=None,
                force_format=None,
                keep_meta=True,
                max_length=300,
                null=True,
                quality=0,
                size=[
                    350,
                    260],
                upload_to=ovp.apps.uploads.models.ImageName('-small')),
        ),
    ]
