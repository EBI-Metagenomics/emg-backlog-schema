# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0005_auto_20180115_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assemblyjob',
            old_name='submission_id',
            new_name='submission',
        ),
    ]
