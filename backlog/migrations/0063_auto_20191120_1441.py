# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-20 14:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    def add_additional_job_statuses(apps, schema_editor):
        AnnotationJobStatus = apps.get_model('backlog', 'AnnotationJobStatus')
        statuses = ['UPLOAD_FAILED', 'SANITY_CHECK_FAILED']
        for status in statuses:
            AnnotationJobStatus(description=status).save()

    dependencies = [
        ('backlog', '0062_auto_20190624_1147'),
    ]

    operations = [
        migrations.RunPython(add_additional_job_statuses)
    ]
