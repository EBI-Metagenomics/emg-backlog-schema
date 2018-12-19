# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-18 15:57
from __future__ import unicode_literals

from django.db import migrations, models


def insert_annotation_job_fixtures(apps, schema_editor):
    AnnotationJobStatus = apps.get_model('backlog', 'AnnotationJobStatus')
    statuses = ['QC_NOT_PASSED', 'UNABLE_TO_PROCESS', 'UNKNOWN']
    for status in statuses:
        AnnotationJobStatus(description=status).save()


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0047_annotationjob_directory'),
    ]

    operations = [
        migrations.RunPython(insert_annotation_job_fixtures),
        migrations.AddField(
            model_name='run',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]