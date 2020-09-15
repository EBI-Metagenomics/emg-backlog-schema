# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-21 10:46
from __future__ import unicode_literals

from django.db import migrations


def create_additional_job_status(apps, schema_editor):
    AnnotationJobStatus = apps.get_model('backlog', 'AnnotationJobStatus')
    AnnotationJobStatus(description='RESTART').save()


def add_new_entry_to_hierarchical_biome_tree(apps, schema_editor):
    Biome = apps.get_model('backlog', 'Biome')
    # Insert new entry
    Biome(biome_id=492, biome_name='Mixed', lft=984, rgt=985, depth=2, lineage='root:Mixed').save()

    try:
        # Update all parent leaves, in this case you only have to update the root entry
        obj = Biome.objects.get(biome_id=0)
        obj.rgt = 985
        obj.save()
    except Biome.DoesNotExist:
        # Look like there is no migration in place yet which populate all the biomes
        pass # skip update in that case

class Migration(migrations.Migration):

    dependencies = [
        ('backlog', '0065_auto_20191205_1422'),
    ]

    operations = [
        migrations.RunPython(create_additional_job_status),
        migrations.RunPython(add_new_entry_to_hierarchical_biome_tree)
    ]