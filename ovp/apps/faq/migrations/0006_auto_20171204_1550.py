# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 17:50
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0005_auto_20171030_1051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'faq', 'verbose_name_plural': 'faq'},
        ),
        migrations.AlterModelOptions(
            name='faqcategory',
            options={'verbose_name': 'faq category', 'verbose_name_plural': 'faq categories'},
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor.fields.RichTextField(default='', max_length=3000, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='faq.FaqCategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=100, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]
