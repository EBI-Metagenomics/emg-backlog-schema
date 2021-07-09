#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from django.utils import timezone

from model_bakery import baker

from backlog.models import AssemblyProteinDB


@pytest.mark.django_db
def test_assembly_proteindb_success():
    pipeline = baker.make("backlog.Pipeline", version=5)
    apdb = baker.make(
        AssemblyProteinDB, status=AssemblyProteinDB.STATUS_COMPLETED, pipeline=pipeline
    )

    assert apdb.status == AssemblyProteinDB.STATUS_COMPLETED
    assert apdb.fail_reason is None
    assert apdb.pipeline == pipeline
    assert timezone.now() >= apdb.last_updated


@pytest.mark.django_db
def test_assembly_proteindb_fail():
    pipeline = baker.make("backlog.Pipeline", version=5)
    apdb = baker.make(
        AssemblyProteinDB,
        status=AssemblyProteinDB.STATUS_FAIL,
        fail_reason=AssemblyProteinDB.FAIL_FASTA_MISSING,
        pipeline=pipeline,
    )

    assert apdb.status == AssemblyProteinDB.STATUS_FAIL
    assert apdb.fail_reason == AssemblyProteinDB.FAIL_FASTA_MISSING
    assert apdb.pipeline == pipeline
    assert timezone.now() >= apdb.last_updated
