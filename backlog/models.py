from django.db import models
from django.utils import timezone


class User(models.Model):
    class Meta:
        db_table = 'User'
        app_label = 'backlog'

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
        app_label = 'backlog'

    primary_accession = models.CharField(max_length=20, unique=True, null=True)
    secondary_accession = models.CharField(max_length=20, unique=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


class Biome(models.Model):
    class Meta:
        db_table = 'Biome'
        app_label = 'backlog'


    biome_id = models.IntegerField(primary_key=True, unique=True)
    biome_name = models.CharField(max_length=60)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    depth = models.IntegerField()
    lineage = models.CharField(max_length=500)


class StudyError(models.Model):
    class Meta:
        db_table = 'StudyErrorType'
        app_label = 'backlog'


    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class Pipeline(models.Model):
    class Meta:
        db_table = 'Pipeline'
        app_label = 'backlog'

    version = models.FloatField(primary_key=True)

    def __str__(self):
        return str(self.version)


class Blacklist(models.Model):
    class Meta:
        db_table = 'Blacklist'
        app_label = 'backlog'


    date_blacklisted = models.DateField(auto_now_add=True)
    pipeline_version = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    error = models.ForeignKey(StudyError, on_delete=models.CASCADE)
    user = models.CharField(max_length=16)
    comment = models.TextField(null=False)


class Study(models.Model):
    class Meta:
        db_table = 'Study'
        app_label = 'backlog'
        unique_together = ('primary_accession', 'secondary_accession')
        verbose_name_plural = 'studies'

    primary_accession = models.CharField(max_length=20)
    secondary_accession = models.CharField(max_length=20)
    title = models.CharField(max_length=4000, null=True)
    description = models.CharField(max_length=4000, null=True, blank=True)
    scientific_name = models.CharField(max_length=200, null=True, blank=True)
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

    def __str__(self):
        return self.primary_accession


class Run(models.Model):
    class Meta:
        db_table = 'Run'
        app_label = 'backlog'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)

    primary_accession = models.CharField(max_length=20, unique=True)
    sample_primary_accession = models.CharField(max_length=20, blank=True, null=True)
    compressed_data_size = models.BigIntegerField(help_text='Sum of filesizes of compressed input. (bytes)', null=True,
                                                  blank=True)
    biome = models.ForeignKey(Biome, to_field='biome_id', db_column='biome_id', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    inferred_biome = models.ForeignKey(Biome, related_name='inferred_run_biome', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    base_count = models.BigIntegerField(null=True, blank=True)
    read_count = models.BigIntegerField(null=True, blank=True)
    instrument_platform = models.CharField(max_length=4000)
    instrument_model = models.CharField(max_length=4000)
    library_strategy = models.CharField(max_length=150, null=True, db_index=True)
    library_layout = models.CharField(max_length=20)
    library_source = models.CharField(max_length=20, null=True)
    ena_last_update = models.DateField(null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.primary_accession


class UserRequest(models.Model):
    class Meta:
        db_table = 'UserRequest'
        app_label = 'backlog'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    first_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    priority = models.IntegerField(default=0)
    rt_ticket = models.IntegerField(unique=True)

    def __str__(self):
        return self.id


# Assemblies received from ENA
class Assembly(models.Model):
    class Meta:
        db_table = 'Assembly'
        app_label = 'backlog'
        verbose_name_plural = 'assemblies'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    primary_accession = models.CharField(max_length=20, unique=True)
    biome = models.ForeignKey(Biome, to_field='biome_id', db_column='biome_id', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    inferred_biome = models.ForeignKey(Biome, db_column='inferred_biome_id', to_field='biome_id', related_name='inferred_assembly_biome', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    public = models.BooleanField(default=True)

    ena_last_update = models.DateField(null=True)


class Assembler(models.Model):
    class Meta:
        db_table = 'Assembler'
        app_label = 'backlog'

    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)


class AssemblyJobStatus(models.Model):
    class Meta:
        db_table = 'AssemblyJobStatus'
        app_label = 'backlog'
        verbose_name_plural = 'assembly job statuses'

    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class AssemblyJobResult(models.Model):
    class Meta:
        db_table = 'AssemblyJobResult'
        app_label = 'backlog'

    execution_time = models.BigIntegerField(
        help_text='Total execution time (including restarts) of the assembler, in seconds.')
    peak_mem = models.BigIntegerField(help_text='Peak memory usage of the assembler, in megabytes.')

    n50 = models.IntegerField()
    l50 = models.IntegerField()
    num_contigs = models.IntegerField()
    assembly_length = models.BigIntegerField()
    largest_contig = models.BigIntegerField()
    coverage = models.FloatField()

    def __str__(self):
        return str(self.id)


class AssemblyJob(models.Model):
    class Meta:
        db_table = 'AssemblyJob'
        app_label = 'backlog'

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
    bam_uploaded = models.NullBooleanField()
    new_ena_assembly = models.CharField(max_length=20, null=True)
    runs = models.ManyToManyField(Run, through='RunAssemblyJob', related_name='assemblyjobs', blank=True)

    def __str__(self):
        return str(self.pk)


# Assembly instances for runs
class RunAssemblyJob(models.Model):
    class Meta:
        db_table = 'RunAssemblyJob'
        app_label = 'backlog'
        unique_together = (('run', 'assembly_job'),)

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    assembly_job = models.ForeignKey(AssemblyJob, on_delete=models.CASCADE)


# Show all runs used to create an assembly
class RunAssembly(models.Model):
    class Meta:
        db_table = 'RunAssembly'
        app_label = 'backlog'
        verbose_name_plural = 'run assemblies'

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)


class AnnotationJobStatus(models.Model):
    class Meta:
        db_table = 'AnnotationJobStatus'
        app_label = 'backlog'

    description = models.CharField(max_length=20)


class AnnotationJob(models.Model):
    class Meta:
        db_table = 'AnnotationJob'
        app_label = 'backlog'

    pipeline = models.ForeignKey(Pipeline, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(AnnotationJobStatus, on_delete=models.DO_NOTHING, db_index=True)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    request = models.ForeignKey(UserRequest, on_delete=models.DO_NOTHING, null=True, db_column='request_id')
    directory = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    runs = models.ManyToManyField(Run, through='RunAnnotationJob', related_name='annotationjobs', blank=True)
    attempt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


# Annotation instance for a run
class RunAnnotationJob(models.Model):
    class Meta:
        db_table = 'RunAnnotationJob'
        app_label = 'backlog'
        unique_together = (('run', 'annotation_job'),)

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)


class AssemblyAnnotationJob(models.Model):
    class Meta:
        db_table = 'AssemblyAnnotationJob'
        app_label = 'backlog'

    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING, related_name='assemblyannotationjobs')
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)


class MonitorAnnotationJobs(models.Model):
    """Model built on top of the view named monitor_annotation_jobs
    """
    class Meta:
        managed = False
        db_table = 'monitor_annotation_jobs' 
        app_label = 'backlog'
        verbose_name_plural = 'monitor annotation jobs'
    
    secondary_accession = models.CharField(max_length=255,  primary_key=True)
    type = models.CharField(max_length=10) # => replace with choices
    email_address = models.EmailField(null=True, blank=True)
    rt_ticket = models.IntegerField(default=0)
    created = models.DateTimeField()
    priority = models.IntegerField()
    public = models.BooleanField(default=False)
    jobs_in_study = models.IntegerField()
    scheduled_jobs = models.IntegerField()
    running_jobs = models.IntegerField()
    failed_jobs = models.IntegerField()
    completed_jobs = models.DecimalField(max_digits=27, decimal_places=3)
    syncing_jobs = models.IntegerField()
    synced_jobs = models.IntegerField()
    uploaded_jobs = models.IntegerField()
    user_notified = models.BooleanField(default=False)
    number_of_biomes = models.IntegerField()
    biome_tagging_complete = models.CharField(max_length=100)

    def __str__(self):
        return self.secondary_accession
