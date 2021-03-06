# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-07 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ovp.apps.channels.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0020_auto_20190701_1827'),
        ('channels', '0009_remove_channel_subchannels'),
        ('core', '0037_auto_20190702_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flair',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name',
                 models.CharField(
                     max_length=100,
                     verbose_name='name')),
                ('value',
                 models.CharField(
                     max_length=100,
                     verbose_name='value')),
                ('channel',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='flair_channel',
                     to='channels.Channel')),
                ('image',
                 models.ForeignKey(
                     blank=True,
                     null=True,
                     on_delete=django.db.models.deletion.CASCADE,
                     to='uploads.UploadedImage',
                     verbose_name='image')),
            ],
            options={
                'verbose_name': 'flair',
            },
            bases=(
                ovp.apps.channels.models.mixins.ChannelCreatorMixin,
                models.Model),
        ),
    ]
