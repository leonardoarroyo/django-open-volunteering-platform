# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-25 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0095_auto_20191125_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyStatusHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('unapplied-by-volunteer', 'Canceled by volunteer'), ('unapplied-by-organization', 'Canceled by organization'), ('confirmed-volunteer', 'Confirmed Volunteer')], max_length=30, verbose_name='status')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Status date')),
            ],
        ),
        migrations.AlterField(
            model_name='apply',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('unapplied-by-volunteer', 'Canceled by volunteer'), ('unapplied-by-organization', 'Canceled by organization'), ('confirmed-volunteer', 'Confirmed Volunteer')], default='applied', max_length=30, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='applystatushistory',
            name='apply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Apply'),
        ),
    ]
