"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from collections import namedtuple
from foundations_model_package.entrypoint_loader import EntrypointLoader

class TestEntrypointLoader(Spec):

    path_exists = let_patch_mock_with_conditional_return('os.path.exists')
    os_chdir = let_patch_mock('os.chdir')
    mock_function = let_mock()
    mock_load_function_from_module = let_patch_mock('foundations_model_package.importlib_wrapper.load_function_from_module')

    @let
    def sys_path(self):
        return self.faker.pylist()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_root(self):
        return self.faker.file_path()

    @let
    def top_level_directory(self):
        return self.faker.word()

    @let
    def mid_level_directory(self):
        return self.faker.word()

    @let
    def lower_level_directory(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    @let
    def entrypoint_name(self):
        return self.faker.word()

    @let
    def manifest(self):
        return {
            'entrypoints': {
                self.entrypoint_name: self.entrypoint
            }
        }

    @let
    def entrypoint(self):
        return {}

    @let
    def job(self):
        job = Mock()
        job.id.return_value = self.job_id
        job.root.return_value = self.job_root
        job.manifest.return_value = self.manifest

        return job

    @set_up
    def set_up(self):
        self.path_exists.return_when(True, self.job_root)
        self.patch('sys.path', self.sys_path)
        self.entrypoint['module'] = self.top_level_directory
        self.entrypoint['function'] = self.function_name

    def test_entrypoint_loader_checks_for_job_root_and_complains_if_it_does_not_exist(self):
        self.path_exists.clear()
        self.path_exists.return_when(False, self.job_root)

        with self.assertRaises(Exception) as error_context:
            EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name)

        self.assertIn(f'Job {self.job_id} not found!', error_context.exception.args)

    def test_entrypoint_loader_adds_job_root_only_to_sys_path_when_module_is_at_top_level(self):
        sys_path_before = list(self.sys_path)
        EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name)
        self.assertEqual([self.job_root] + sys_path_before, self.sys_path)

    def test_entrypoint_loader_chdir_to_job_root(self):
        EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name)
        self.os_chdir.assert_called_once_with(self.job_root)

    def test_entrypoint_loader_adds_job_root_and_module_parent_to_sys_path_when_module_is_not_at_top_level(self):
        self.entrypoint['module'] = f'{self.top_level_directory}.{self.lower_level_directory}'
        sys_path_before = list(self.sys_path)
        EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name)
        self.assertEqual([f'{self.job_root}/{self.top_level_directory}', self.job_root] + sys_path_before, self.sys_path)

    def test_entrypoint_loader_adds_job_root_and_module_parent_to_sys_path_when_module_nested_further(self):
        self.entrypoint['module'] = f'{self.top_level_directory}.{self.mid_level_directory}.{self.lower_level_directory}'
        sys_path_before = list(self.sys_path)
        EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name)
        self.assertEqual([f'{self.job_root}/{self.top_level_directory}/{self.mid_level_directory}', self.job_root] + sys_path_before, self.sys_path)

    def test_entrypoint_loader_returns_function_from_module_as_configured(self):
        mock_load_function_from_module = self.patch('foundations_model_package.importlib_wrapper.load_function_from_module', ConditionalReturn())
        mock_load_function_from_module.return_when(self.mock_function, self.top_level_directory, self.function_name)
        self.assertEqual(self.mock_function, EntrypointLoader(self.job).entrypoint_function(self.entrypoint_name))