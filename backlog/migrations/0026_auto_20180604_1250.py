# Generated by Django 2.0.3 on 2018-06-04 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0025_auto_20180604_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study',
            name='scientific_name',
        ),
        migrations.RemoveField(
            model_name='study',
            name='tax_id',
        ),
    ]
