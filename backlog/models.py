from django.db import models
from django.utils import timezone


class Submission(models.Model):
    class Meta:
        db_table = 'Submission'

    primary_accession = models.CharField(max_length=20, unique=True, null=True)
    secondary_accession = models.CharField(max_length=20, unique=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=timezone.now)


class Biome(models.Model):
    class Meta:
        db_table = 'Biome'

    biome_id = models.IntegerField(unique=True)
    biome_name = models.CharField(max_length=60)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    depth = models.IntegerField()
    lineage = models.CharField(max_length=500)


class StudyError(models.Model):
    class Meta:
        db_table = 'StudyErrorType'

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class Pipeline(models.Model):
    class Meta:
        db_table = 'Pipeline'

    version = models.FloatField(primary_key=True)


class Blacklist(models.Model):
    class Meta:
        db_table = 'Blacklist'

    date_blacklisted = models.DateField(auto_now_add=True)
    pipeline_version = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    error = models.ForeignKey(StudyError, on_delete=models.CASCADE)
    user = models.CharField(max_length=16)
    comment = models.TextField(null=False)


class Study(models.Model):
    class Meta:
        db_table = 'Study'

    primary_accession = models.CharField(max_length=20, unique=True)
    secondary_accession = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=4000, null=True)
    public = models.NullBooleanField()
    hold_date = models.DateField(null=True)
    first_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    ena_last_update = models.DateField(null=True)
    tax_id = models.CharField(max_length=4000, null=True)
    scientific_name = models.CharField(max_length=4000, null=True)
    mixs_compliant = models.NullBooleanField()
    pubmed = models.TextField(null=True)
    webin = models.CharField(max_length=100, null=True)
    blacklisted = models.ForeignKey(Blacklist, on_delete=models.CASCADE, null=True)


class Run(models.Model):
    class Meta:
        db_table = 'Run'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    primary_accession = models.CharField(max_length=20)
    compressed_data_size = models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)')
    biome = models.ForeignKey(Biome, to_field='biome_id', db_column='biome_id', on_delete=models.DO_NOTHING, null=True)
    base_count = models.BigIntegerField()
    read_count = models.BigIntegerField()
    instrument_platform = models.CharField(max_length=4000)
    instrument_model = models.CharField(max_length=4000)
    library_strategy = models.CharField(max_length=150, null=True)
    library_layout = models.CharField(max_length=20)
    library_source = models.CharField(max_length=20, null=True)
    ena_last_update = models.DateField(null=True)


# Assemblies received from ENA
class Assembly(models.Model):
    class Meta:
        db_table = 'Assembly'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    primary_accession = models.CharField(max_length=20)


class Assembler(models.Model):
    class Meta:
        db_table = 'Assembler'

    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)


class AssemblyJobStatus(models.Model):
    class Meta:
        db_table = 'AssemblyJobStatus'

    description = models.CharField(max_length=20)


class AssemblyJobResult(models.Model):
    class Meta:
        db_table = 'AssemblyJobResult'

    execution_time = models.BigIntegerField(
        help_text='Total execution time (including restarts) of the assembler, in seconds.')
    peak_mem = models.BigIntegerField(help_text='Peak memory usage of the assembler, in megabytes.')

    n50 = models.IntegerField()
    l50 = models.IntegerField()
    num_contigs = models.IntegerField()
    assembly_length = models.BigIntegerField()
    largest_contig = models.BigIntegerField()
    coverage = models.FloatField()


class AssemblyJob(models.Model):
    class Meta:
        db_table = 'AssemblyJob'

    assembler = models.ForeignKey(Assembler, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(AssemblyJobStatus, on_delete=models.DO_NOTHING)
    submission = models.ForeignKey(Submission, on_delete=models.DO_NOTHING, null=True)

    user = models.CharField(max_length=16, null=True)

    input_size = models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)')
    reason = models.TextField(null=True,
                              help_text='Filled iff assembly will not be submitted to ENA, specifies the reason why.')
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], null=True)
    result = models.ForeignKey(AssemblyJobResult, on_delete=models.CASCADE, null=True)

    uploaded_to_ena = models.NullBooleanField()
    new_ena_assembly = models.CharField(max_length=20, null=True)
    runs = models.ManyToManyField(Run, through='RunAssemblyJob', related_name='assemblyjobs', blank=True)


# Assembly instances for runs
class RunAssemblyJob(models.Model):
    class Meta:
        db_table = 'RunAssemblyJob'
        unique_together = (('run', 'assembly_job'),)

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    assembly_job = models.ForeignKey(AssemblyJob, on_delete=models.CASCADE)


# Show all runs used to create an assembly
class RunAssembly(models.Model):
    class Meta:
        db_table = 'RunAssembly'

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)


class AnnotationStatus(models.Model):
    class Meta:
        db_table = 'AnnotationStatus'

    description = models.CharField(max_length=20)


class AnnotationJob(models.Model):
    class Meta:
        db_table = 'AnnotationJob'

    pipeline = models.ForeignKey(Pipeline, on_delete=models.DO_NOTHING)
    exec_status = models.ForeignKey(AnnotationStatus, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    user = models.CharField(max_length=16, null=True)


# Annotation instance for a run
class RunAnnotationJob(models.Model):
    class Meta:
        db_table = 'RunAnnotationJob'

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)


class AssemblyAnnotationJob(models.Model):
    class Meta:
        db_table = 'AssemblyAnnotationJob'

    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)
