# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-06 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0046_auto_20181128_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotationjob',
            name='directory',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
