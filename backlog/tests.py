# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.db import connection
from django.core.management import call_command

import sys
import os
import yaml

sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('../assembly_script'))
print (os.getcwd())
try:
    from ebi_metagenomics_assembly.lib import new_db
except ImportError:
    print('==== ERROR: MISSING PROJECT ====')
    print('ebi_metagenomics_assembly must be cloned in a relative path')
    print('run mkdir ../../assembly_script && cd ../../assembly_script && git clone <assembly_script_url>')
    sys.exit(1)


class AssemblyScriptDBTest(TestCase):
    prim_accession = 'PRJ123123'
    sec_accession = 'ERP001736'
    with open(os.path.join("backlog", "test_data", "assembly.yaml"), "r") as f:
        data = yaml.load(f)

    def setUp(self):
        call_command("loaddata", "status.yaml", verbosity=0)
        call_command("loaddata", "biomes.yaml", verbosity=0)

    # Runs the full assembly process, up to the decision to upload/not upload to ena
    def full_assembly_process(self, cur):
        # Verify project insertion works
        self.assertFalse(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))
        self.assertTrue(new_db.insert_project_into_db(cur, self.data['study']))
        self.assertTrue(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))

        self.assertFalse(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))
        self.assertTrue(new_db.insert_run_into_db(cur, self.data['run']))
        self.assertTrue(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))

        self.assertTrue(new_db.insert_assembly_init(connection, cur, self.data['start_assembly']))

        # Verify assembly is started
        self.assertTrue(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))
        assembler_name = self.data['start_assembly']['assembler_name']
        assembler_version = self.data['start_assembly']['assembler_version']
        self.assertTrue(new_db.is_run_assembling_with_version(cur, self.data['run']['primary_accession'],
                                                              assembler_name,
                                                              assembler_version))

        # Verify number of finished assemblies is 0
        self.assertTrue(len(new_db.get_assembled_runs(cur, self.data['study']['secondary_accession'])) == 0)

        self.assertTrue(new_db.set_assembly_finished(connection, cur, self.data['finish_assembly']))

        # Verify number of finished assemblies is 1
        self.assertTrue(len(new_db.get_assembled_runs(cur, self.data['study']['secondary_accession'])) == 1)

        self.assertFalse(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))

        self.assertFalse(new_db.is_run_assembling_with_version(cur, self.data['run']['primary_accession'],
                                                               assembler_name,
                                                               assembler_version))

    # Start to end of the assembly pipeline, from job selection to ena upload (with mocked project/run insertions
    def test_full_pipeline_with_ena(self):
        with connection.cursor() as cur:
            self.full_assembly_process(cur)
            # Verify number of uploaded assemblies is 0
            self.assertTrue(len(new_db.get_uploaded_assemblies(cur, self.data['study']['secondary_accession'])) == 0)

            self.assertTrue(
                len(new_db.get_undetermined_assemblies(cur, self.data['study']['secondary_accession'])) == 1)

            self.assertTrue(new_db.set_ena_upload(cur, self.data['ena_upload_accepted']))

            # Verify number of uploaded assemblies is 1
            self.assertTrue(len(new_db.get_uploaded_assemblies(cur, self.data['study']['secondary_accession'])) == 1)

            self.assertTrue(
                len(new_db.get_undetermined_assemblies(cur, self.data['study']['secondary_accession'])) == 0)

    def test_full_pipeline_without_ena(self):
        with connection.cursor() as cur:
            self.full_assembly_process(cur)
            # Verify number of uploaded assemblies is 0
            self.assertTrue(len(new_db.get_uploaded_assemblies(cur, self.data['study']['secondary_accession'])) == 0)

            self.assertTrue(
                len(new_db.get_undetermined_assemblies(cur, self.data['study']['secondary_accession'])) == 1)

            self.assertTrue(new_db.set_ena_upload(cur, self.data['ena_upload_denied']))

            # Verify number of uploaded assemblies is still 0
            self.assertTrue(len(new_db.get_uploaded_assemblies(cur, self.data['study']['secondary_accession'])) == 0)

            self.assertTrue(
                len(new_db.get_undetermined_assemblies(cur, self.data['study']['secondary_accession'])) == 0)

    def test_assembly_failure(self):
        with connection.cursor() as cur:
            self.assertFalse(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))
            self.assertTrue(new_db.insert_project_into_db(cur, self.data['study']))
            self.assertTrue(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))

            self.assertFalse(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))
            self.assertTrue(new_db.insert_run_into_db(cur, self.data['run']))
            self.assertTrue(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))

            self.assertTrue(new_db.insert_assembly_init(connection, cur, self.data['start_assembly']))
            assembly_job_id = cur.lastrowid

            # Verify assembly is started
            self.assertTrue(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))

            # Set assemblyJob failure
            self.assertTrue(new_db.set_assembly_failure(cur, assembly_job_id))
            self.assertFalse(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))

    def test_deleting_assemblyJob_does_not_remove_run(self):
        with connection.cursor() as cur:
            self.assertFalse(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))
            self.assertTrue(new_db.insert_project_into_db(cur, self.data['study']))
            self.assertTrue(new_db.is_project_in_backlog(cur, self.data['study']['secondary_accession']))

            self.assertFalse(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))
            self.assertTrue(new_db.insert_run_into_db(cur, self.data['run']))
            self.assertTrue(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))

            self.assertTrue(new_db.insert_assembly_init(connection, cur, self.data['start_assembly']))
            assembly_job_id = cur.lastrowid

            # Verify assembly is started
            self.assertTrue(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))

            # Remove assembly (eg: decide not to assemble run)
            self.assertTrue(new_db.remove_assemblyJob(cur, assembly_job_id))
            self.assertFalse(new_db.is_run_assembling(cur, self.data['run']['primary_accession']))

            # Verify AssemblyJob was also removed
            cur.execute("SELECT id FROM AssemblyJob WHERE id=%s;", (assembly_job_id,))
            result = cur.fetchall()
            self.assertTrue(len(result) == 0)

            # Verify run was note removed
            self.assertTrue(new_db.is_run_in_backlog(cur, self.data['run']['primary_accession']))
