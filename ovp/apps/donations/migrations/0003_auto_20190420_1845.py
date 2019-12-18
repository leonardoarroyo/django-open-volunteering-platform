# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-20 21:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0055_organization_allow_donations'),
        ('donations', '0002_subscription_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(
                default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(
                auto_now_add=True,
                default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='date_modified',
            field=models.DateTimeField(
                auto_now=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='organization',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to='organizations.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(
                default=None,
                max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]