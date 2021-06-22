from django.db import models
from django.utils import timezone


class User(models.Model):
    class Meta:
        db_table = 'User'
        app_label='backlog'

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
        app_label='backlog'


    primary_accession = models.CharField(max_length=20, unique=True, null=True)
    secondary_accession = models.CharField(max_length=20, unique=True, null=True)
    uuid = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)


class Biome(models.Model):
    class Meta:
        db_table = 'Biome'
        app_label='backlog'


    biome_id = models.IntegerField(primary_key=True, unique=True)
    biome_name = models.CharField(max_length=60)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    depth = models.IntegerField()
    lineage = models.CharField(max_length=500)


class StudyError(models.Model):
    class Meta:
        db_table = 'StudyErrorType'
        app_label='backlog'


    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class Pipeline(models.Model):
    class Meta:
        db_table = 'Pipeline'
        app_label='backlog'


    version = models.FloatField(primary_key=True)


class Blacklist(models.Model):
    class Meta:
        db_table = 'Blacklist'
        app_label='backlog'


    date_blacklisted = models.DateField(auto_now_add=True)
    pipeline_version = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    error = models.ForeignKey(StudyError, on_delete=models.CASCADE)
    user = models.CharField(max_length=16)
    comment = models.TextField(null=False)


class Study(models.Model):
    class Meta:
        db_table = 'Study'
        app_label='backlog'
        unique_together = ('primary_accession', 'secondary_accession')

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


class Run(models.Model):
    class Meta:
        db_table = 'Run'
        app_label='backlog'

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


class UserRequest(models.Model):
    class Meta:
        db_table = 'UserRequest'
        app_label='backlog'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    first_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    priority = models.IntegerField(default=0)
    rt_ticket = models.IntegerField(unique=True)


class AssemblyType(models.Model):
    class Meta:
        db_table = 'AssemblyType'
        app_label = 'backlog'

    assembly_type = models.CharField(max_length=80, unique=True, null=False)

    def __str__(self):
        return self.assembly_type


# Assemblies received from ENA
class Assembly(models.Model):
    class Meta:
        db_table = 'Assembly'
        app_label='backlog'

    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    primary_accession = models.CharField(max_length=20, unique=True)
    biome = models.ForeignKey(Biome, to_field='biome_id', db_column='biome_id', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    inferred_biome = models.ForeignKey(Biome, db_column='inferred_biome_id', to_field='biome_id', related_name='inferred_assembly_biome', on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    public = models.BooleanField(default=True)
    ena_last_update = models.DateField(null=True)
    assembly_type = models.ForeignKey('AssemblyType', db_column='assembly_type_id', on_delete=models.DO_NOTHING, blank=True, null=True)


class Assembler(models.Model):
    class Meta:
        db_table = 'Assembler'
        app_label='backlog'

    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)


class AssemblyJobStatus(models.Model):
    class Meta:
        db_table = 'AssemblyJobStatus'
        app_label='backlog'

    description = models.CharField(max_length=100)


class AssemblyJobResult(models.Model):
    class Meta:
        db_table = 'AssemblyJobResult'
        app_label='backlog'

    execution_time = models.BigIntegerField(
        help_text='Total execution time (including restarts) of the assembler, in seconds.')
    peak_mem = models.BigIntegerField(help_text='Peak memory usage of the assembler, in megabytes.')

    n50 = models.IntegerField()
    l50 = models.IntegerField()
    num_contigs = models.IntegerField()
    assembly_length = models.BigIntegerField()
    largest_contig = models.BigIntegerField()
    coverage = models.FloatField()
    # average depth of coverage of the assembly
    coverage_depth = models.FloatField()


class AssemblyJob(models.Model):
    class Meta:
        db_table = 'AssemblyJob'
        app_label='backlog'

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


# Assembly instances for runs
class RunAssemblyJob(models.Model):
    class Meta:
        db_table = 'RunAssemblyJob'
        app_label='backlog'
        unique_together = (('run', 'assembly_job'),)

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    assembly_job = models.ForeignKey(AssemblyJob, on_delete=models.CASCADE)


# Show all runs used to create an assembly
class RunAssembly(models.Model):
    class Meta:
        db_table = 'RunAssembly'
        app_label='backlog'

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)


class AnnotationJobStatus(models.Model):
    class Meta:
        db_table = 'AnnotationJobStatus'
        app_label='backlog'

    description = models.CharField(max_length=20)


class AnnotationJob(models.Model):

    pipeline = models.ForeignKey(Pipeline, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(AnnotationJobStatus, on_delete=models.DO_NOTHING, db_index=True)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    request = models.ForeignKey(UserRequest, on_delete=models.DO_NOTHING, null=True, db_column='request_id')
    directory = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    runs = models.ManyToManyField(Run, through='RunAnnotationJob', related_name='annotationjobs', blank=True)
    attempt = models.IntegerField(default=0)

    # Pipeline execution result status.
    # For example the pipeline may find no CDS so most steps
    # aren't going to be executed for this data set.
    RESULT_NO_TAX = 'no_tax'
    RESULT_NO_QC = 'no_qc'
    RESULT_NO_CDS = 'no_cds'
    # pipeline completed all the stages
    RESULT_FULL = 'full'
    RESULT_CHOICES = (
        (RESULT_NO_TAX, 'No Taxonomy results'),
        (RESULT_NO_QC, 'Failed QC'),
        (RESULT_NO_CDS, 'No CDS found'),
        (RESULT_FULL, 'No problems')
    )

    result_status = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        blank=True, null=True)

    class Meta:
        db_table = 'AnnotationJob'
        app_label = 'backlog'


# Annotation instance for a run
class RunAnnotationJob(models.Model):
    class Meta:
        db_table = 'RunAnnotationJob'
        app_label='backlog'
        unique_together = (('run', 'annotation_job'),)

    run = models.ForeignKey(Run, on_delete=models.DO_NOTHING)
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)


class AssemblyAnnotationJob(models.Model):
    class Meta:
        db_table = 'AssemblyAnnotationJob'
        app_label = 'backlog'

    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING, related_name='assemblyannotationjobs')
    annotation_job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE)

    # success
    PROTEIN_DB_SUCCESS = 1
    # fail
    PROTEIN_DB_FAIL = 0
    PROTEIN_DB_NO_PROTEIN_FASTA = 2
    PROTEIN_DB_PATH_ERROR = 3
    NO_DIRECTORY = 4
    SUPPRESSED = 5

    PROTEIN_DB_CHOICES = (
        (PROTEIN_DB_SUCCESS, 'Retrofitting finished without errors'),
        (PROTEIN_DB_FAIL, 'Retrofitting was not run OR failed by unknown reason' ),
        (PROTEIN_DB_NO_PROTEIN_FASTA, 'There is no faa fasta file with predicted proteins'),
        (PROTEIN_DB_PATH_ERROR, 'Invalid path, failed to find the results folder'),
        (NO_DIRECTORY, 'Can not detect directory in EMG table'),
        (SUPPRESSED, 'Study was suppressed by ENA')
    )

    protein_db = models.IntegerField(choices=PROTEIN_DB_CHOICES, default=PROTEIN_DB_FAIL)
