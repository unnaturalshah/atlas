"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _expect_code(status_code):
    def _decorator(method):
        def _wrapped_method(*args, **kwargs):
            response = method(*args, **kwargs)

            if response.status_code != status_code:
                raise CronJobSchedulerError(response.text)
        
        return _wrapped_method
    return _decorator

class CronJobScheduler(object):

    def __init__(self, host=None, port=None):
        import importlib
        
        if host is None:
            host = 'localhost'
        
        if port is None:
            port = 5000

        self._scheduler_uri = f'http://{host}:{port}'
        self._raw_api = importlib.import_module('requests')

    def pause_job(self, job_id):
        self._change_job_status(job_id, 'paused')
    
    def resume_job(self, job_id):
        self._change_job_status(job_id, 'active')

    def schedule_job(self, job_id, spec, schedule, job_bundle_path, metadata=None, gpu_spec=None):
        pass

    def get_jobs(self):
        pass

    def get_job(self, job_id):
        return self._raw_api.get(self._job_uri(job_id)).json()

    def update_job_schedule(self, job_id):
        pass

    @_expect_code(204)
    def delete_job(self, job_id):
        return self._raw_api.delete(self._job_uri(job_id))

    @_expect_code(204)
    def _change_job_status(self, job_id, status):
        return self._raw_api.put(self._job_uri(job_id), json={'status': status})

    def _job_uri(self, job_id):
        return f'{self._scheduler_uri}/scheduled_jobs/{job_id}'

class CronJobSchedulerError(Exception):
    pass