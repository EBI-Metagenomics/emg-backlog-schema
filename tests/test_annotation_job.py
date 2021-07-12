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

from model_bakery import baker

from backlog.models import AnnotationJob


@pytest.mark.django_db
def test_annotation_job_success():
    pipeline = baker.make("backlog.Pipeline", version=5)
    ann_job_status = baker.make("backlog.AnnotationJobStatus")
    request = baker.make("backlog.UserRequest")

    ann_job = baker.make(
        AnnotationJob,
        status=ann_job_status,
        pipeline=pipeline,
        request=request,
        priority=AnnotationJob.PRIORITY_LOW,
        result_status=AnnotationJob.RESULT_NO_CDS,
    )

    assert ann_job.status == ann_job_status
    assert ann_job.pipeline == pipeline
    assert ann_job.request == request
    assert ann_job.priority == AnnotationJob.PRIORITY_LOW
    assert ann_job.result_status == AnnotationJob.RESULT_NO_CDS
    assert ann_job.runs.count() == 0

    ann_job.result_status = AnnotationJob.RESULT_FULL
    ann_job.save()
    assert ann_job.result_status == AnnotationJob.RESULT_FULL
