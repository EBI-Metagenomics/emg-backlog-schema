# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-05 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0078_auto_20210813_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='assemblyproteindb',
            name='legacy',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='New accession for legacy assembly'),
        ),
    ]