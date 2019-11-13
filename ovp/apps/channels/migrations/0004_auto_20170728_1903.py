# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-28 19:03
from __future__ import unicode_literals

from django.db import migrations

def foward_func(apps, schema_editor):
    Channel = apps.get_model("channels", "Channel")
    channel = Channel.objects.create(name="default", slug="default")

    # We freeze default channels skills and causes because
    # post_save signals are not sent from migrations
    from ovp.apps.core.models.skill import SKILLS
    from ovp.apps.core.models.cause import CAUSES

    Skill = apps.get_model("core", "Skill")
    Cause = apps.get_model("core", "Cause")

    for skill in SKILLS:
      Skill.objects.create(name=skill, channel=channel)

    for cause in CAUSES:
      Cause.objects.create(name=cause, channel=channel)

    return True

def rewind_func(apps, schema_editor):
    Channel = apps.get_model("channels", "Channel")
    Channel.objects.all().delete()
    return True


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_channel_slug'),
        ('core', '0014_auto_20170825_1914'),
    ]

    operations = [
        migrations.RunPython(foward_func, rewind_func)
    ]
