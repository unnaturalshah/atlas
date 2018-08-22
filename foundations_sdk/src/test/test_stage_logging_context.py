"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.stage_logging_context import StageLoggingContext


class TestStageLoggingContext(unittest.TestCase):

    class MockLogger(object):

        def __init__(self):
            self.key = None
            self.value = None

        def log_metric(self, key, value):
            self.key = key
            self.value = value

    def test_log_metric_logs_key(self):
        logger = self.MockLogger()
        context = StageLoggingContext(logger)

        context.log_metric('loss', 0.554)
        self.assertEqual('loss', logger.key)

    def test_log_metric_logs_key_different_key(self):
        logger = self.MockLogger()
        context = StageLoggingContext(logger)

        context.log_metric('accuracy', 0.554)
        self.assertEqual('accuracy', logger.key)

    def test_log_metric_logs_value(self):
        logger = self.MockLogger()
        context = StageLoggingContext(logger)

        context.log_metric('loss', 0.554)
        self.assertEqual(0.554, logger.value)

    def test_log_metric_logs_value_different_value(self):
        logger = self.MockLogger()
        context = StageLoggingContext(logger)

        context.log_metric('loss', 0.1554)
        self.assertEqual(0.1554, logger.value)

    def test_change_logger_changes_logger(self):
        logger = self.MockLogger()
        logger_two = self.MockLogger()
        context = StageLoggingContext(logger)

        with context.change_logger(logger_two):
            context.log_metric('loss', 0.1554)
            self.assertEqual(0.1554, logger_two.value)

    def test_change_logger_resets_logger(self):
        logger = self.MockLogger()
        logger_two = self.MockLogger()
        context = StageLoggingContext(logger)

        with context.change_logger(logger_two):
            pass

        context.log_metric('loss', 0.1554)
        self.assertEqual(0.1554, logger.value)
