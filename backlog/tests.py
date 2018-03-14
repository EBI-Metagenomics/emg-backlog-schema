# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import yaml

from django.test import TestCase
from django.core.management import call_command
from django.db import models
from backlog.models import *

sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('../assembly_script'))
print(os.getcwd())
try:
    from assembly_pipeline.lib import db
except ImportError:
    print('==== ERROR: MISSING PROJECT ====')
    print('assembly_pipeline must be cloned in a relative path')
    print('run mkdir ../../assembly_script && cd ../../assembly_script && git clone <assembly_script_url>')
    sys.exit(1)


class AssemblyScriptDBTest(TestCase):
    prim_accession = 'PRJ123123'
    sec_accession = 'ERP001736'
    DAO = db.DAO('default')

    with open(os.path.join("backlog", "test_data", "assembly.yaml"), "r") as f:
        data = yaml.load(f)

    with open(os.path.join("backlog", "test_data", "assembly2.yaml"), "r") as f:
        data2 = yaml.load(f)

    def setUp(self):
        call_command("loaddata", "status.yaml", verbosity=0)
        call_command("loaddata", "biomes.yaml", verbosity=0)

    # Runs the full assembly process, up to the decision to upload/not upload to ena
    def full_assembly_process(self, data, additional_run=False):
        # Verify project insertion works
        if not additional_run:
            self.assertFalse(self.DAO.is_study_in_backlog(data['study']['secondary_accession']))
            self.assertTrue(self.DAO.insert_study_into_db(data['study']))
        self.assertTrue(self.DAO.is_study_in_backlog(data['study']['secondary_accession']))

        self.assertFalse(self.DAO.is_run_in_backlog(data['run']['primary_accession']))
        self.assertTrue(self.DAO.insert_run_into_db(data['run']))
        self.assertTrue(self.DAO.is_run_in_backlog(data['run']['primary_accession']))

        self.assertTrue(self.DAO.insert_assembly_init(data['start_assembly']))

        # Verify assembly is started
        self.assertTrue(self.DAO.is_run_assembling(data['run']['primary_accession']))
        assembler_name = data['start_assembly']['assembler_name']
        assembler_version = data['start_assembly']['assembler_version']
        self.assertTrue(self.DAO.is_run_assembling_with_version(data['run']['primary_accession'],
                                                                assembler_name,
                                                                assembler_version))

        # Verify number of finished assemblies is 0
        num_assembled = len(self.DAO.get_assembled_runs(data['study']['secondary_accession']))
        if not additional_run:
            self.assertEquals(num_assembled, 0)

        self.assertTrue(self.DAO.set_assembly_finished(data['finish_assembly']))

        # Verify number of finished assemblies is 1
        self.assertEquals(len(self.DAO.get_assembled_runs(data['study']['secondary_accession'])), num_assembled + 1)

        self.assertFalse(self.DAO.is_run_assembling(data['run']['primary_accession']))

        self.assertFalse(self.DAO.is_run_assembling_with_version(data['run']['primary_accession'],
                                                                 assembler_name,
                                                                 assembler_version))

    # Start to end of the assembly pipeline, from job selection to ena upload (with mocked project/run insertions
    def test_full_pipeline_with_ena(self):
        self.full_assembly_process(self.data)
        # Verify number of uploaded assemblies is 0
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data['study']['secondary_accession'])), 0)

        self.assertEqual(len(self.DAO.get_undetermined_assemblies(self.data['study']['secondary_accession'])), 1)

        self.assertTrue(self.DAO.set_ena_upload(self.data['ena_upload_accepted']))
        self.assertTrue(self.DAO.was_assembly_submitted(self.data['run']['primary_accession'],
                                                        self.data['start_assembly']['assembler_name']))

        # Verify number of uploaded assemblies is 1
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data['study']['secondary_accession'])), 1)

        self.assertEqual(len(self.DAO.get_undetermined_assemblies(self.data['study']['secondary_accession'])), 0)

    def test_full_pipeline_without_ena(self):
        self.full_assembly_process(self.data)
        # Verify number of uploaded assemblies is 0
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data['study']['secondary_accession'])), 0)

        self.assertEqual(
            len(self.DAO.get_undetermined_assemblies(self.data['study']['secondary_accession'])), 1)

        self.assertTrue(self.DAO.set_ena_upload(self.data['ena_upload_denied']))

        # Verify number of uploaded assemblies is still 0
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data['study']['secondary_accession'])), 0)

        self.assertEqual(
            len(self.DAO.get_undetermined_assemblies(self.data['study']['secondary_accession'])), 0)

    def test_add_assembly_to_submission(self):
        self.test_full_pipeline_with_ena()
        # Verify number of uploaded assemblies is 1
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data['study']['secondary_accession'])), 1)

        # Verify second assembly is assembled and ready to upload
        self.full_assembly_process(self.data2, additional_run=True)
        self.assertEqual(len(self.DAO.get_undetermined_assemblies(self.data2['study']['secondary_accession'])), 1)

        # Upload second assembly and add to project
        self.assertTrue(self.DAO.set_ena_upload(self.data2['ena_upload_accepted']))
        self.assertTrue(self.DAO.was_assembly_submitted(self.data2['run']['primary_accession'],
                                                        self.data2['start_assembly']['assembler_name']))

        # Verify both assemblies are uploaded
        self.assertEqual(len(self.DAO.get_uploaded_assemblies(self.data2['study']['secondary_accession'])), 2)
        self.assertEqual(
            len(self.DAO.get_undetermined_assemblies(self.data2['study']['secondary_accession'])), 0)

        # Verify both runs are under same submission
        submissions = self.DAO.get_existing_ena_study_accessions(self.data2['study']['secondary_accession']).values()
        self.assertEquals(len(submissions), 1)
        self.assertEquals(submissions[0]['primary_accession'],
                          self.data['ena_upload_accepted']['new_study_primary_accession'])
        self.assertEquals(submissions[0]['primary_accession'],
                          self.data2['ena_upload_accepted']['new_study_primary_accession'])

        self.assertEquals(submissions[0]['secondary_accession'],
                          self.data['ena_upload_accepted']['new_study_secondary_accession'])
        self.assertEquals(submissions[0]['secondary_accession'],
                          self.data2['ena_upload_accepted']['new_study_secondary_accession'])



        # def test_

        # def test_assembly_failure(self):
        #     self.assertFalse(self.DAO.is_study_in_backlog(self.data['study']['secondary_accession']))
        #     self.assertTrue(self.DAO.insert_study_into_db(self.data['study']))
        #     self.assertTrue(self.DAO.is_study_in_backlog(self.data['study']['secondary_accession']))
        #
        #     self.assertFalse(self.DAO.is_run_in_backlog(self.data['run']['primary_accession']))
        #     self.assertTrue(self.DAO.insert_run_into_db(self.data['run']))
        #     self.assertTrue(self.DAO.is_run_in_backlog(self.data['run']['primary_accession']))
        #
        #     self.assertTrue(self.DAO.insert_assembly_init(self.data['start_assembly']))
        #
        #     # Verify assembly is started
        #     self.assertTrue(self.DAO.is_run_assembling(self.data['run']['primary_accession']))
        #
        #     del self.data['start_assembly']['priority']
        #     del self.data['start_assembly']['input_size']
        #     # Set assemblyJob failure
        #     self.assertTrue(self.DAO.set_assembly_failure(**self.data['start_assembly']))
        #     self.assertFalse(self.DAO.is_run_assembling(self.data['run']['primary_accession']))



        # def test_deleting_assemblyJob_does_not_remove_run(self):
        #     self.assertFalse(self.DAO.is_study_in_backlog(self.data['study']['secondary_accession']))
        #     self.assertTrue(self.DAO.insert_study_into_db(self.data['study']))
        #     self.assertTrue(self.DAO.is_study_in_backlog(self.data['study']['secondary_accession']))
        #
        #     self.assertFalse(self.DAO.is_run_in_backlog(self.data['run']['primary_accession']))
        #     self.assertTrue(self.DAO.insert_run_into_db(self.data['run']))
        #     self.assertTrue(self.DAO.is_run_in_backlog(self.data['run']['primary_accession']))
        #
        #     self.assertTrue(self.DAO.insert_assembly_init(self.data['start_assembly']))
        #
        #     # Verify assembly is started
        #     self.assertTrue(self.DAO.is_run_assembling(self.data['run']['primary_accession']))
        #
        #     # Remove assembly (eg: decide not to assemble run)
        #     self.assertTrue(self.DAO.remove_assemblyJob(**self.data['start_assembly']))
        #     self.assertFalse(self.DAO.is_run_assembling(self.data['run']['primary_accession']))
        #
        #     # Verify AssemblyJob was also removed
        #     self.assertFalse(self.DAO.is_assembly_in_backlog(**self.data['start_assembly']))
        #
        #     # Verify run was note removed
        #     self.assertTrue(self.DAO.is_run_in_backlog(self.data['run']['primary_accession']))
