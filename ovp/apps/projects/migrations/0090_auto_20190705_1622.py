# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-05 19:22
from __future__ import unicode_literals

from django.db import migrations


def foward_func(apps, schema_editor):
    VolunteerRole = apps.get_model('projects', 'VolunteerRole')
    Apply = apps.get_model('projects', 'Apply')

    for vr in VolunteerRole.objects.all():
        vr.applied_count = Apply.objects.filter(
            role=vr, status__in=[
                "applied", "confirmed-volunteer"]).count()
        vr.save()


def rewind_func():
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0089_auto_20190703_1401'),
    ]

    operations = [
        migrations.RunPython(foward_func, rewind_func)
    ]
