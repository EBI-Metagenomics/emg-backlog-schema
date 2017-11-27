# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
                ('user', models.CharField(max_length=16, null=True)),
            ],
            options={
                'db_table': 'AnnotationJob',
            },
        ),
        migrations.CreateModel(
            name='AnnotationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'AnnotationStatus',
            },
        ),
        migrations.CreateModel(
            name='Assembler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('version', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Assembler',
            },
        ),
        migrations.CreateModel(
            name='Assembly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_accession', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Assembly',
            },
        ),
        migrations.CreateModel(
            name='AssemblyAnnotationJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.AnnotationJob')),
                ('assembly', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Assembly')),
            ],
            options={
                'db_table': 'AssemblyAnnotationJob',
            },
        ),
        migrations.CreateModel(
            name='AssemblyJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=16, null=True)),
                ('input_size', models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)')),
                ('reason', models.TextField(help_text='Filled iff assembly will not be submitted to ENA, specifies the reason why.', null=True)),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], null=True)),
                ('uploaded_to_ena', models.NullBooleanField()),
                ('new_ena_study_prima_accession', models.CharField(max_length=20, null=True)),
                ('new_ena_study_secon_accession', models.CharField(max_length=20, null=True)),
                ('new_ena_assembly', models.CharField(max_length=20, null=True)),
                ('assembler', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Assembler')),
            ],
            options={
                'db_table': 'AssemblyJob',
            },
        ),
        migrations.CreateModel(
            name='AssemblyJobResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_time', models.BigIntegerField(help_text='Total execution time (including restarts) of the assembler, in seconds.')),
                ('peak_mem', models.BigIntegerField(help_text='Peak memory usage of the assembler, in megabytes.')),
                ('n50', models.IntegerField()),
                ('l50', models.IntegerField()),
                ('num_contigs', models.IntegerField()),
                ('assembly_length', models.BigIntegerField()),
                ('largest_contig', models.BigIntegerField()),
                ('coverage', models.FloatField()),
            ],
            options={
                'db_table': 'AssemblyJobResult',
            },
        ),
        migrations.CreateModel(
            name='AssemblyJobStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'AssemblyJobStatus',
            },
        ),
        migrations.CreateModel(
            name='Biome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biome_id', models.IntegerField(unique=True)),
                ('biome_name', models.CharField(max_length=60)),
                ('lft', models.IntegerField()),
                ('rgt', models.IntegerField()),
                ('depth', models.IntegerField()),
                ('lineage', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Biome',
            },
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_blacklisted', models.DateField(auto_now_add=True)),
                ('user', models.CharField(max_length=16)),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'Blacklist',
            },
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('version', models.FloatField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Pipeline',
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_accession', models.CharField(max_length=20)),
                ('compressed_data_size', models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)')),
                ('base_count', models.BigIntegerField()),
                ('read_count', models.BigIntegerField()),
                ('instrument_platform', models.CharField(max_length=4000)),
                ('instrument_model', models.CharField(max_length=4000)),
                ('library_layout', models.CharField(max_length=20)),
                ('biome', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Biome')),
            ],
            options={
                'db_table': 'Run',
            },
        ),
        migrations.CreateModel(
            name='RunAnnotationJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.AnnotationJob')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Run')),
            ],
            options={
                'db_table': 'RunAnnotationJob',
            },
        ),
        migrations.CreateModel(
            name='RunAssembly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Assembly')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Run')),
            ],
            options={
                'db_table': 'RunAssembly',
            },
        ),
        migrations.CreateModel(
            name='RunAssemblyJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.AssemblyJob')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.Run')),
            ],
            options={
                'db_table': 'RunAssemblyJob',
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_accession', models.CharField(max_length=20, unique=True)),
                ('secondary_accession', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('public', models.NullBooleanField()),
                ('hold_date', models.DateField(null=True)),
                ('first_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('tax_id', models.CharField(max_length=4000, null=True)),
                ('scientific_name', models.CharField(max_length=4000, null=True)),
                ('library_strategy', models.CharField(max_length=150, null=True)),
                ('mixs_compliant', models.NullBooleanField()),
                ('pubmed', models.TextField(null=True)),
                ('webin', models.CharField(max_length=100, null=True)),
                ('blacklisted', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backlog.Blacklist')),
            ],
            options={
                'db_table': 'Study',
            },
        ),
        migrations.CreateModel(
            name='StudyError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'StudyErrorType',
            },
        ),
        migrations.AddField(
            model_name='run',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.Study'),
        ),
        migrations.AddField(
            model_name='blacklist',
            name='error',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.StudyError'),
        ),
        migrations.AddField(
            model_name='blacklist',
            name='pipeline_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.Pipeline'),
        ),
        migrations.AddField(
            model_name='assemblyjob',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backlog.AssemblyJobResult'),
        ),
        migrations.AddField(
            model_name='assemblyjob',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.AssemblyJobStatus'),
        ),
        migrations.AddField(
            model_name='assembly',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backlog.Study'),
        ),
        migrations.AddField(
            model_name='annotationjob',
            name='exec_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.AnnotationStatus'),
        ),
        migrations.AddField(
            model_name='annotationjob',
            name='pipeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='backlog.Pipeline'),
        ),
    ]
