"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

@skip
class TestUserDefinedSchedulerImage(Spec):

    @let
    def scheduler_host(self):
        from foundations_contrib.global_state import config_manager
        return config_manager['remote_host']
    
    @let
    def config(self):
        import yaml

        with open('scheduler_acceptance/fixtures/user_defined_scheduler_image/config/scheduler.template.config.yaml', 'r') as file:
            config = yaml.load(file.read())

        config['results_config']['redis_end_point'] = f'redis://{self.scheduler_host}:6379'
        config['ssh_config']['host'] = self.scheduler_host
        return config

    @let
    def redis_connection(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        import yaml
        import foundations

        with open('scheduler_acceptance/fixtures/user_defined_scheduler_image/config/scheduler.config.yaml', 'w+') as file:
            file.write(yaml.dump(self.config))

        foundations.set_job_resources(num_gpus=0)
        job = foundations.deploy(env='scheduler', job_directory='scheduler_acceptance/fixtures/user_defined_scheduler_image/')
        job.wait_for_deployment_to_complete()
        self.job_id = job.job_name()

    def test_can_run_job_with_custom_image(self):
        import json

        key = f'jobs:{self.job_id}:parameters'
        serialized_parameters = self.redis_connection.get(key)
        parameters = json.loads(serialized_parameters)

        self.assertEqual(self.job_id, parameters['job_id'])
