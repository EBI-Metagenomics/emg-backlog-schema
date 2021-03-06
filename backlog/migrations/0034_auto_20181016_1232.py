# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-16 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0033_auto_20181016_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('priority', models.IntegerField(default=0)),
                ('webin_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.User')),
            ],
            options={
                'db_table': 'UserRequest',
            },
        ),
        migrations.RemoveField(
            model_name='annotationjob',
            name='user',
        ),
        migrations.RemoveField(
            model_name='assemblyjob',
            name='user',
        ),
        migrations.AddField(
            model_name='annotationjob',
            name='request_id',
            field=models.ForeignKey(db_column='request_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.UserRequest'),
        ),
        migrations.AddField(
            model_name='assemblyjob',
            name='request_id',
            field=models.ForeignKey(db_column='request_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.UserRequest'),
        ),
    ]
