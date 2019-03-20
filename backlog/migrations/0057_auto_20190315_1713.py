# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-15 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0056_auto_20190315_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='description',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='study',
            name='scientific_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
