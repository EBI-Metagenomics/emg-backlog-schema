# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-01 15:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0035_userrequest_rt_ticket'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnnotationStatus',
            new_name='AnnotationJobStatus',
        ),
        migrations.AlterModelTable(
            name='annotationjobstatus',
            table='AnnotationJobStatus',
        ),
    ]
