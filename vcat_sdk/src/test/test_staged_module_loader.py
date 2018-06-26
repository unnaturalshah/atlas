import unittest
from vcat.staged_module_loader import StagedModuleLoader
from vcat.stage_connector_wrapper import StageConnectorWrapper


class TestStagedModuleLoader(unittest.TestCase):
    class MockModule(object):
        def __init__(self):
            self._pi = None
            self.__file__ = None
            self.dumps = lambda x: None

    def test_loader_is_loader(self):
        from importlib.abc import Loader

        result = StagedModuleLoader(None)
        self.assertIsInstance(result, Loader)

    def test_create_module_returns_none(self):
        result = StagedModuleLoader(None).create_module(None)
        self.assertEqual(None, result)

    def test_exec_module_loads_vars(self):
        import pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        self.assertEqual(pickle.__file__, module.__file__)

    def test_exec_module_loads_vars_from_different_module(self):
        import random
        module = self.MockModule()
        StagedModuleLoader(random).exec_module(module)
        self.assertEqual(random._pi, module._pi)

    def test_exec_module_creates_stages_from_function(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps('hello')
        self.assertIsInstance(result, StageConnectorWrapper)

    def test_exec_module_stage_function_executes_function(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps('hello')()
        self.assertTrue(pickle.loads(result), 'hello')

    def test_exec_module_stage_function_supports_kwargs(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps(obj='hello')()
        self.assertTrue(pickle.loads(result), 'hello')
