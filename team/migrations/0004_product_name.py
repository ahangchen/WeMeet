# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20160714_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
