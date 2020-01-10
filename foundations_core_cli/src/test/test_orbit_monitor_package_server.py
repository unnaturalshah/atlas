"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *


class TestOrbitMonitorPackageServer(Spec):

    mock_log_manager = let_patch_mock('foundations_contrib.global_state.log_manager')
    mock_logger = Mock()

    @let_now
    def redis(self):
        return self.patch('foundations_contrib.global_state.redis_connection')

    @set_up
    def set_up(self):
        self.mock_config_manager = self.patch('foundations_contrib.foundations_contrib.global_state.config_manager')
        self.mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000'}

        mock_get_logger = ConditionalReturn()
        mock_get_logger.return_when(self.mock_logger, 'foundations_core_cli.orbit_monitor_package_server')
        self.mock_log_manager.get_logger = mock_get_logger

        self.patch('builtins.print')
        self.patch('foundations_contrib.set_job_resources.set_job_resources')

    @let
    def cwd(self):
        return '.'

    @let
    def command(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def env(self):
        return self.faker.word()

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let_now
    def cron_job_scheduler(self):
        mock_cron_job_scheduler = Mock()
        mock_cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
        mock_cron_job_scheduler_class.return_value = mock_cron_job_scheduler
        return mock_cron_job_scheduler
    
    @let_now
    def load(self):
        return self.patch('foundations_core_cli.job_submission.config.load')

    def test_pause_called_cron_job_scheduler_pause_job(self):
        from foundations_core_cli.orbit_monitor_package_server import pause
        pause(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.pause_job.assert_called_once_with(self.monitor_package_id)

    def test_pause_called_cron_job_scheduler_resume_job(self):
        from foundations_core_cli.orbit_monitor_package_server import resume
        resume(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.resume_job.assert_called_once_with(self.monitor_package_id)

    def test_pause_uses_update_config_with_values_from_env(self):
        from foundations_core_cli.orbit_monitor_package_server import pause
        pause(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)
    
    def test_resume_uses_update_config_with_values_from_env(self):
        from foundations_core_cli.orbit_monitor_package_server import resume
        resume(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)

    def test_delete_called_cron_job_scheduler_pause_job(self):
        from foundations_core_cli.orbit_monitor_package_server import delete
        delete(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.delete_job.assert_called_once_with(self.monitor_package_id)

    def test_delete_uses_update_config_with_values_from_env(self):
        from foundations_core_cli.orbit_monitor_package_server import delete
        delete(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)

    def test_get_called_cron_job_scheduler_get_job_with_params_with_project_name_as_parameter(self):
        from foundations_core_cli.orbit_monitor_package_server import get_by_project
        get_by_project(self.project_name, self.env)
        self.cron_job_scheduler.get_job_with_params.assert_called_once_with({'project':  self.project_name})

    def test_start_handles_no_job_config_case(self):
        from foundations_core_cli.orbit_monitor_package_server import start

        self.patch('foundations_core_cli.orbit_monitor_package_server.get_by_project')
        mock_yaml_load = self.patch('yaml.load')
        mock_yaml_load.side_effect = IOError
        with self.assertRaises(KeyError):
            start(self.cwd, self.command, None, None, None)

    def test_start_fails_with_correct_error_if_monitor_already_exists(self):
        from foundations_core_cli.orbit_monitor_package_server import start

        mock_get_by_project = self.patch('foundations_core_cli.orbit_monitor_package_server.get_by_project', ConditionalReturn())
        mock_get_by_project.return_when({f'{self.project_name}-{self.monitor_name}': ''}, self.project_name)

        with self.assertRaises(ValueError) as error:
            start(self.cwd, self.command, self.project_name, self.monitor_name, self.env)

        self.assertEqual('Monitor already exists', str(error.exception))

    def test_monitor_create_logs_correct_message_when_start_called(self):
        self.mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000', 'worker_container_overrides': {'args': ''}}

        from foundations_core_cli.orbit_monitor_package_server import start

        mock_get_by_project = self.patch('foundations_core_cli.orbit_monitor_package_server.get_by_project')
        mock_get_by_project.return_value = []

        self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.job_bundle')
        mock_submit_job_bundle = self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.submit_job_bundle')

        with self.assertRaises(RuntimeError):
            start(self.cwd, self.command, None, None, None)

        self.mock_logger.info.assert_called_with('Creating monitor ...')

    def test_monitor_create_logs_correct_message_when_job_bundle_submitted(self):
        self.mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000', 'worker_container_overrides': {'args': ''}}

        from foundations_core_cli.orbit_monitor_package_server import start

        mock_get_by_project = self.patch('foundations_core_cli.orbit_monitor_package_server.get_by_project')
        mock_get_by_project.return_value = []

        self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.job_bundle')
        mock_submit_job_bundle = self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.submit_job_bundle')
        mock_response = Mock()
        mock_response.status_code = 200
        mock_submit_job_bundle.return_value = mock_response

        with self.assertRaises(KeyError):
            start(self.cwd, self.command, None, None, None)

        self.mock_logger.info.assert_called_with('Job bundle submitted.')

    def test_monitor_create_logs_correct_message_when_job_scheduled(self):
        self.mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000', 'worker_container_overrides': {'args': ''}}

        from foundations_core_cli.orbit_monitor_package_server import start

        mock_get_by_project = self.patch('foundations_core_cli.orbit_monitor_package_server.get_by_project')
        mock_get_by_project.return_value = []

        self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.job_bundle')
        mock_submit_job_bundle = self.patch('foundations_local_docker_scheduler_plugin.bundle_deployment.submit_job_bundle')
        mock_response = Mock()
        mock_response.status_code = 200
        mock_submit_job_bundle.return_value = mock_response

        mock_cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler', ConditionalReturn())
        mock_cron_job_scheduler = Mock()
        mock_cron_job_scheduler.schedule_job.return_value = Mock()
        mock_cron_job_scheduler_class.return_when(mock_cron_job_scheduler, 'https://localhost:5000')

        self.patch('foundations_core_cli.orbit_monitor_package_server._get_monitor_job_spec')
        self.patch('foundations_core_cli.orbit_monitor_package_server._get_monitor_gpu_spec')

        start(self.cwd, self.command, None, None, None)

        info_call = call('Monitor scheduled.')

        self.mock_logger.info.assert_has_calls([info_call])