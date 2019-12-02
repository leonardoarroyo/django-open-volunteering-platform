# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-29 02:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import ovp.apps.channels.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0060_merge_20191017_1335'),
        ('channels', '0009_remove_channel_subchannels'),
        ('donations', '0013_auto_20191017_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.CharField(max_length=80)),
                ('backend', models.CharField(max_length=80)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_channel', to='channels.Channel')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
            ],
            options={
                'verbose_name': 'seller',
            },
            bases=(ovp.apps.channels.models.mixins.ChannelCreatorMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='seller',
            unique_together=set([('organization', 'seller_id')]),
        ),
    ]
