"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.stage_cache import StageCache


class MockCache(object):

    def __init__(self):
        self.cache = {}
        self.meta_data = {}

    def get_option(self, key):
        from foundations.nothing import Nothing
        return self.cache.get(key, Nothing())

    def set(self, key, value, metadata):
        from foundations.something import Something
        self.cache[key] = Something(value)
        self.meta_data[key] = metadata
        return value


class MockCacheManager(object):

    def __init__(self):
        self._cache = MockCache()

    def cache(self):
        return self._cache

    def default_cache_enabled(self):
        return False


class MockVersion(object):

    def __init__(self, major):
        self.major = major


class TestStageCache(unittest.TestCase):

    class MockStage(object):

        def __init__(self, uuid):
            self._uuid = uuid

        def uuid(self):
            return self._uuid

    class MockLiveArgument(object):

        def __init__(self, hash):
            self._hash = hash

        def hash(self):
            return self._hash

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_cache_name(self):
        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        self.assertEqual(
            '6bbe865851bc74298ad8bbae0113745a618eb27f', stage_cache.cache_name())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_cache_name_different_name(self):
        stage = self.MockStage('some other uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        self.assertEqual(
            '4632ba0ef31b2b9022a3991625cc075f9025ee31', stage_cache.cache_name())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_nothing(self):
        from foundations.nothing import Nothing

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        self.assertEqual(Nothing(), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_something_when_set(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        cache_manager.cache().set('6bbe865851bc74298ad8bbae0113745a618eb27f', 'some value', {})
        self.assertEqual(Something('some value'), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_nothing_when_set_but_cache_disabled(self):
        from foundations.global_state import cache_manager
        from foundations.nothing import Nothing

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(False), ())
        cache_manager.cache().set('6bbe865851bc74298ad8bbae0113745a618eb27f', 'some value', {})
        self.assertEqual(Nothing(), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_nothing_when_set_different_value(self):
        from foundations.global_state import cache_manager
        from foundations.nothing import Nothing

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        cache_manager.cache().set('77777777777777777777777777777777777777777', 'some value', {})
        self.assertEqual(Nothing(), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_something_when_set_with_different_uuid(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        cache_manager.cache().set('fa7d3bb37675cc2388eb118a2b1c0d893d5e586a', 'some value', {})
        self.assertEqual(Something('some value'), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_something_when_set_with_different_arguments(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        argument = self.MockLiveArgument('hello?')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), (argument, ))
        cache_manager.cache().set('b5d5d3dfe880a4d68ac0f5587c1aa640bbd1674f', 'some value', {})
        self.assertEqual(Something('some value'), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_something_when_set_with_multiple_arguments(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        argument = self.MockLiveArgument('hello?')
        argument_two = self.MockLiveArgument('hello again')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(pipeline_context, stage, self._make_config(
            True), (argument, argument_two))
        cache_manager.cache().set('8f1888f6f97d96c03255f1a6fd61b762bbc4fc6e', 'some value', {})
        self.assertEqual(Something('some value'), stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_returns_something_when_set_with_different_value(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        cache_manager.cache().set(
            'fa7d3bb37675cc2388eb118a2b1c0d893d5e586a', 'some different value', {})
        self.assertEqual(Something('some different value'),
                         stage_cache.fetch_option())

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_something_when_set(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            '6bbe865851bc74298ad8bbae0113745a618eb27f')
        self.assertEqual(Something('some value'), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_includes_meta_data_when_set(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        pipeline_context.file_name = 'actually the job name'
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().meta_data['6bbe865851bc74298ad8bbae0113745a618eb27f']
        self.assertEqual({'job_uuid': 'actually the job name'}, result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_includes_meta_data_when_set_different_meta_data(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        pipeline_context.file_name = 'actually the job name, but a different one'
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().meta_data['6bbe865851bc74298ad8bbae0113745a618eb27f']
        self.assertEqual({'job_uuid': 'actually the job name, but a different one'}, result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_nothing_when_set_but_cache_disabled(self):
        from foundations.global_state import cache_manager
        from foundations.nothing import Nothing

        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(False), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            '6bbe865851bc74298ad8bbae0113745a618eb27f')
        self.assertEqual(Nothing(), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_nothing_and_returns_the_value_when_set_but_cache_disabled(self):
        stage = self.MockStage('some uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(False), ())
        result = stage_cache.submit('some value')
        self.assertEqual('some value', result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_something_when_set_with_different_uuid(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            'fa7d3bb37675cc2388eb118a2b1c0d893d5e586a')
        self.assertEqual(Something('some value'), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(2))
    def test_cache_sets_something_when_set_with_different_version(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            '5aa7bd0dc3561e68b3fc788c2a762f22e1bb2374')
        self.assertEqual(Something('some value'), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_something_when_set_with_different_arguments(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        argument = self.MockLiveArgument('hello?')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), (argument, ))
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            'b5d5d3dfe880a4d68ac0f5587c1aa640bbd1674f')
        self.assertEqual(Something('some value'), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_something_when_set_with_multiple_arguments(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        argument = self.MockLiveArgument('hello?')
        argument_two = self.MockLiveArgument('hello again')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(pipeline_context, stage, self._make_config(
            True), (argument, argument_two))
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            '8f1888f6f97d96c03255f1a6fd61b762bbc4fc6e')
        self.assertEqual(Something('some value'), result)

    @patch('foundations.global_state.cache_manager', MockCacheManager())
    @patch('sys.version_info', MockVersion(3))
    def test_cache_sets_something_when_set_with_different_value(self):
        from foundations.global_state import cache_manager
        from foundations.something import Something

        stage = self.MockStage('some different uuid')
        pipeline_context = self._make_pipeline_context()
        stage_cache = StageCache(
            pipeline_context, stage, self._make_config(True), ())
        stage_cache.submit('some value')
        result = cache_manager.cache().get_option(
            'fa7d3bb37675cc2388eb118a2b1c0d893d5e586a')
        self.assertEqual(Something('some value'), result)

    def _make_config(self, cached):
        from foundations.stage_config import StageConfig

        config = StageConfig()
        if cached:
            config.enable_caching()

        return config

    def _make_pipeline_context(self):
        from foundations.pipeline_context import PipelineContext
        return PipelineContext()