# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-17 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0050_annotationjob_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='assemblyjob',
            name='cram_uploaded',
            field=models.NullBooleanField(),
        ),
    ]
