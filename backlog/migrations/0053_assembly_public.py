# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-20 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0052_annotationjob_runs'),
    ]

    operations = [
        migrations.AddField(
            model_name='assembly',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
