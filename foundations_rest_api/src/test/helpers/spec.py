"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from test.helpers import set_up, tear_down
from test.helpers.mock_mixin import MockMixin

class Spec(unittest.TestCase, MockMixin):
    
    def setUp(self):
        for setup_method in self._setup_methods():
            setup_method(self)

    def _setup_methods(self):
        for function in self.__class__.__dict__.values():
            if isinstance(function, set_up):
                yield function
    
    def tearDown(self):
        for tear_down_method in self._tear_down_methods():
            tear_down_method(self)
        self._mock_tear_down()

    def _tear_down_methods(self):
        for function in self.__class__.__dict__.values():
            if isinstance(function, tear_down):
                yield function
