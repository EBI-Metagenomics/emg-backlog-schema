# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2021-08-12 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0075_auto_20210723_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationjob',
            name='result_status',
            field=models.CharField(blank=True, choices=[('no_tax', 'No Taxonomy results'), ('no_qc', 'Failed QC'), ('no_cds', 'No CDS found'), ('full', 'No problems'), ('no_cds_tax', 'No CDS or taxonomy found')], max_length=10, null=True),
        ),
    ]