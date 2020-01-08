"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from auth_acceptance.config import setup_auth_home_config
setup_auth_home_config()

# from auth_acceptance.test_auth_via_cli import TestAuthViaClient
from auth_acceptance.test_submit_with_auth import TestSubmitWithAuth
