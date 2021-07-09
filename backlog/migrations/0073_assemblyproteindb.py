# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-09 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0072_auto_20210422_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyProteinDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Completed'), (0, 'Failed')], verbose_name='status')),
                ('fail_reason', models.IntegerField(blank=True, choices=[(1, 'Missing protein fasta file'), (2, 'Invalid fasta file path'), (3, 'Assembly results directory is missing'), (4, 'Suppressed assembly')], null=True, verbose_name='fail_reason')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last updated')),
                ('assembly', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Assembly')),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Pipeline')),
            ],
        ),
    ]
