# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'webin_id',
        'registered',
        'email_address',
        'first_name',
        'surname',
        'first_created',
    )


@admin.register(models.Submission)
class Submission(admin.ModelAdmin):
    list_display = (
        'primary_accession',
        'secondary_accession',
        'uuid',
        'created',
    )


@admin.register(models.Biome)
class Biome(admin.ModelAdmin):
    list_display = (
        'biome_id',
        'lft',
        'rgt',
        'depth',
        'lineage'
    )


@admin.register(models.StudyError)
class StudyError(admin.ModelAdmin):
    pass


@admin.register(models.Pipeline)
class Pipeline(admin.ModelAdmin):
    pass


@admin.register(models.Blacklist)
class Blacklist(admin.ModelAdmin):
    list_display = (
        'user',
        'error',
        'pipeline_version'
    )


@admin.register(models.Study)
class Study(admin.ModelAdmin):
    list_display = (
        'primary_accession',
        'secondary_accession',
        'title'
    )
    date_hierarchy = 'last_updated'
    list_filter = (
        'public',
    )
    search_fields = [
        'primary_accession',
        'secondary_accession',
        'title',
        'description'
    ]


@admin.register(models.Run)
class Run(admin.ModelAdmin):
    list_display = (
        'primary_accession',
    )
    search_fields = [
        'primary_accession',
    ]


@admin.register(models.UserRequest)
class UserRequest(admin.ModelAdmin):
    list_display = (
        'user',
        'first_created',
        'last_updated',
        'priority',
        'rt_ticket',
    )
    date_hierarchy = 'last_updated'
    search_fields = [
        'user__webin_id',
        'user__email_address',
        'user__first_name',
        'user__surname',
        'secondary_accession',
    ]


@admin.register(models.Assembly)
class Assembly(admin.ModelAdmin):
    list_display = (
        'primary_accession',
        'study',
        'biome',
        'inferred_biome',
        'public',
        'ena_last_update',
    )
    date_hierarchy = 'ena_last_update'
    search_fields = [
        'primary_accession',
        'biome__biome_name',
        'biome__lineage',
        'study__primary_accession',
        'study__secondary_accession',
        'study__description',
        'study__webin'
    ]


@admin.register(models.Assembler)
class Assembler(admin.ModelAdmin):
    list_display = (
        'name',
        'version'
    )


@admin.register(models.AssemblyJobStatus)
class AssemblyJobStatus(admin.ModelAdmin):
     pass


@admin.register(models.AssemblyJobResult)
class AssemblyJobResult(admin.ModelAdmin):
    list_display = (
        'n50',
        'num_contigs',
        'assembly_length',
        'largest_contig',
        'coverage',
        'execution_time',
        'peak_mem'
    )


@admin.register(models.AssemblyJob)
class AssemblyJob(admin.ModelAdmin):
    list_display = (
        'id',
        'assembler',
        'status',
        'submission',
        'priority',
        'uploaded_to_ena',
        'bam_uploaded',
        'new_ena_assembly'
    )
    list_filter = (
        'assembler',
        'status',
        'priority',
        'uploaded_to_ena',
        'bam_uploaded'
    )
    search_fields = [
        'id',
        'submission__primary_accession',
        'submission__secondary_accession',
        'user__webin_id',
        'user__email_address',
        'user__first_name',
        'user__surname',
    ]


@admin.register(models.RunAssemblyJob)
class RunAssemblyJob(admin.ModelAdmin):
    pass


@admin.register(models.RunAssembly)
class RunAssembly(admin.ModelAdmin):
    pass


@admin.register(models.AnnotationJobStatus)
class AnnotationJobStatus(admin.ModelAdmin):
    pass


@admin.register(models.AnnotationJob)
class AnnotationJob(admin.ModelAdmin):
    list_display = (
        'id',
        'pipeline',
        'status',
        'priority',
        'request',
        'last_updated',
        'attempt'
    )
    list_filter = (
        'pipeline__version',
        'status',
    )
    date_hierarchy = 'last_updated'
    search_fields = [
        'id',
    ]


@admin.register(models.RunAnnotationJob)
class RunAnnotationJob(admin.ModelAdmin):
    pass


@admin.register(models.AssemblyAnnotationJob)
class AssemblyAnnotationJob(admin.ModelAdmin):
    pass


@admin.register(models.MonitorAnnotationJobs)
class MonitorAnnotationJobs(admin.ModelAdmin):
    list_display_links = None
    list_display = (
        'secondary_accession',
        'type',
        'created',
        'priority',
        'public',
        'jobs_in_study',
        'scheduled_jobs',
        'running_jobs',
        'failed_jobs',
        'completed_jobs',
        'syncing_jobs',
        'synced_jobs',
        'uploaded_jobs',
        'user_notified',
        'number_of_biomes',
        'biome_tagging_complete'
    )
    date_hierarchy = 'created'
    list_filter = (
        'type',
        'priority',
        'public',
        'user_notified'
    )
    search_fields = [
        'secondary_accession',
        'email_address'
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
