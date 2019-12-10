"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import acceptance.config
from acceptance.test_duplicate_job_source import TestDuplicateJobSource
from acceptance.test_recursion_limit import TestRecursionLimit
from acceptance.test_job_data_producers import TestJobDataProducers
from acceptance.test_cli_init import TestCLIInit
from acceptance.test_archive_jobs import TestArchiveJobs
from acceptance.test_local_obfuscate_jobs import TestLocalObfuscateJobs
from acceptance.test_set_environment import TestSetEnvironment
from acceptance.test_class_stage_deployment import TestClassStageDeployment
from acceptance.test_log_metric_outside_stage import TestLogMetricOutsideStage
from acceptance.test_annotate_without_stage import TestAnnotateWithoutStage
from acceptance.test_can_load_parameters import TestCanLoadParameters
from acceptance.test_generate_random_parameters import TestGenerateRandomParameters
from acceptance.test_save_artifact import TestSaveArtifact
from acceptance.test_syncable_directory import TestSyncableDirectory
from acceptance.test_can_run_locally import TestCanRunLocally
from acceptance.test_result_job_bundle import TestResultJobBundle
from foundations_contrib.global_state import module_manager

def _append_module():
    import sys
    module_manager.append_module(sys.modules[__name__])


_append_module()