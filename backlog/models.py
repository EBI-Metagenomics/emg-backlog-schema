from django.db import models
from django.utils import timezone


class User(models.Model):
    class Meta:
        db_table = 'User'

    webin_id = models.CharField("ENA's submission account id", max_length=15, unique=True, primary_key=True)
    registered = models.BooleanField(
        "A copy of ENA's ROLE_METAGENOME_SUBMITTER flag. Set to True if submitter is registered with EMG.",
        default=False)
    consent_given = models.BooleanField(
        "A copy of ENA's ROLE_METAGENOME_ANALYSIS flag. Set to True if submitter gave permission to access and analyse their private data.",
        default=False)
    email_address = models.CharField("Submitters email address.", max_length=200)
    first_name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=50, null=True)
    first_created = models.DateTimeField(auto_now_add=True, null=True)


class Submission(models.Model):
    class Meta:
        db_table = 'Submission'

    primary_accession = models.CharField(max_length=20, unique=True, null=True)
    secondary_accession = models.CharField(max_length=20, unique=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


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
        unique_together = ('primary_accession', 'secondary_accession')

    primary_accession = models.CharField(max_length=20)
    secondary_accession = models.CharField(max_length=20)
    title = models.CharField(max_length=4000, null=True)
    public = models.BooleanField(default=True)
    hold_date = models.DateField(null=True)
    first_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    ena_last_update = models.DateField(null=True)
    mixs_compliant = models.NullBooleanField()
    pubmed = models.TextField(null=True)
    webin = models.CharField(max_length=100, null=True)
    blacklisted = models.ForeignKey(Blacklist, on_delete=models.CASCADE, null=True)
    submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


class Run(models.Model):
    class Meta:
        db_table = 'Run'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    primary_accession = models.CharField(max_length=20, unique=True)
    sample_primary_accession = models.CharField(max_length=20, blank=True, null=True)
    compressed_data_size = models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)', null=True,
                                                  blank=True)
    biome = models.ForeignKey(Biome, to_field='biome_id', db_column='biome_id', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    biome_validated = models.BooleanField(default=False)
    base_count = models.BigIntegerField()
    read_count = models.BigIntegerField()
    instrument_platform = models.CharField(max_length=4000)
    instrument_model = models.CharField(max_length=4000)
    library_strategy = models.CharField(max_length=150, null=True)
    library_layout = models.CharField(max_length=20)
    library_source = models.CharField(max_length=20, null=True)
    ena_last_update = models.DateField(null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    public = models.BooleanField(default=True)


class UserRequest(models.Model):
    class Meta:
        db_table = 'UserRequest'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    first_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    priority = models.IntegerField(default=0)
    rt_ticket = models.IntegerField(unique=True)


# Assemblies received from ENA
class Assembly(models.Model):
    class Meta:
        db_table = 'Assembly'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    primary_accession = models.CharField(max_length=20, unique=True)
    ena_last_update = models.DateField(null=True)


class Assembler(models.Model):
    class Meta:
        db_table = 'Assembler'

    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)


class AssemblyJobStatus(models.Model):
    class Meta:
        db_table = 'AssemblyJobStatus'

    description = models.CharField(max_length=100)


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

    request_id = models.ForeignKey(UserRequest, on_delete=models.DO_NOTHING, null=True, db_column='request_id', )
    directory = models.CharField(max_length=255, null=True, blank=True)

    input_size = models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)')
    reason = models.TextField(null=True,
                              help_text='Filled iff assembly will not be submitted to ENA, specifies the reason why.')
    requester = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], null=True)
    result = models.ForeignKey(AssemblyJobResult, on_delete=models.CASCADE, null=True)
    estimated_peak_mem = models.BigIntegerField(help_text='Estimated peak memory usage of the assembler, in megabytes.',
                                                null=True)

    uploaded_to_ena = models.NullBooleanField()
    cram_uploaded = models.NullBooleanField()
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


class AnnotationJobStatus(models.Model):
    class Meta:
        db_table = 'AnnotationJobStatus'

    description = models.CharField(max_length=20)


class AnnotationJob(models.Model):
    class Meta:
        db_table = 'AnnotationJob'

    pipeline = models.ForeignKey(Pipeline, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(AnnotationJobStatus, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    request = models.ForeignKey(UserRequest, on_delete=models.DO_NOTHING, null=True, db_column='request_id')
    directory = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    runs = models.ManyToManyField(Run, through='RunAnnotationJob', related_name='annotationjobs', blank=True)


# Annotation instance for a run
class RunAnnotationJob(models.Model):
    class Meta:
        db_table = 'RunAnnotationJob'
        unique_together = (('run', 'annotation_job'),)

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)


class AssemblyAnnotationJob(models.Model):
    class Meta:
        db_table = 'AssemblyAnnotationJob'

    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)
