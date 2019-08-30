"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import os
import typing

import foundations
from foundations_spec import Spec, let, set_up
from foundations_rest_api.global_state import app_manager


class TestTensorboardEndpoint(Spec):
    url = '/api/v2beta/upload_to_tensorboard'
    client = app_manager.app().test_client()

    @let
    def scheduler_host(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['remote_host']

    @let
    def redis_url(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['redis_url']
    
    @let
    def config(self):
        return {
            'results_config': {
                'redis_end_point': self.redis_url
            },
            'ssh_config': {
                'host': self.scheduler_host,
                'port': 31222,
                'code_path': '/jobs',
                'key_path': '~/.ssh/id_foundations_scheduler',
                'user': 'job-uploader'
            }
        }

    @let
    def deployment(self) -> foundations.DeploymentWrapper:
        return foundations.submit(
            project_name='test', 
            entrypoint='tensorboard_job', 
            job_dir='scheduler_acceptance/fixtures/tensorboard_job'
        )

    @let
    def job_id(self) -> let:
        return self.deployment.job_name()

    @let
    def sync_directory(self) -> str:
        archives = os.environ['ARCHIVE_ROOT']
        return f'{archives}/sync'

    @set_up
    def set_up(self):
        import yaml
        from acceptance.cleanup import cleanup
        cleanup()

        with open('scheduler_acceptance/fixtures/tensorboard_job/config/submission/scheduler.config.yaml', 'w+') as file:
            file.write(yaml.dump(self.config))
        self.deployment.wait_for_deployment_to_complete()

    def test_upload_to_tensorflow(self):
        data = self.client.post(self.url, json={'tensorboard_locations': [{'job_id': self.job_id, 'synced_directory': 'tb_data'}]})
        self.assertEqual(data.get_json(), f'Success! the specified jobs: [{self.job_id}] have been sent to tensorboard')

