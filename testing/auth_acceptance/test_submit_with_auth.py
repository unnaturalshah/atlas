"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 12 2019
"""


from foundations_spec import *
from foundations_contrib.utils import foundations_home
import os
import os.path
from os.path import expanduser, join

class TestSubmitWithAuth(Spec):
    
    @set_up
    def set_up(self):
        credential_filepath = expanduser(join(foundations_home(), "credentials.yaml"))
        if os.path.exists(credential_filepath):
            os.remove(credential_filepath)

    def test_submit_through_cli_fails_if_not_authenticated(self):
        import subprocess

        result = subprocess.run('foundations submit scheduler auth_acceptance/fixtures foundations_job.py',\
             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        self.assertIn('Token is not valid', result.stdout.decode().strip())
