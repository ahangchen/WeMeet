# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuinfo',
            name='edu_background',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='stuinfo',
            name='grade',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='stuinfo',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stuinfo',
            name='location',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='stuinfo',
            name='major',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
