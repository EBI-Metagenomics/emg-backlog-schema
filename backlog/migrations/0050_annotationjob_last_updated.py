# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-19 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0049_auto_20181218_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotationjob',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
