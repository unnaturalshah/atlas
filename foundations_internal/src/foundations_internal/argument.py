"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Argument(object):

    @staticmethod
    def generate_from(value, name):
        if isinstance(value, Argument):
            return value

        parameter = Argument._generate_parameter_from(value, name)
        return Argument(name, parameter)

    @staticmethod
    def _generate_parameter_from(value, name):
        from foundations.hyperparameter import Hyperparameter
        from foundations.stage_connector_wrapper import StageConnectorWrapper
        from foundations_contrib.constant_parameter import ConstantParameter
        from foundations_contrib.dynamic_parameter import DynamicParameter
        from foundations_contrib.stage_parameter import StageParameter
        from foundations_contrib.list_parameter import ListParameter
        from foundations_contrib.dict_parameter import DictParameter

        if isinstance(value, Hyperparameter):
            if value.name is None:
                value.name = name
            return  DynamicParameter(value)

        if isinstance(value, StageConnectorWrapper):
            return StageParameter(value)
        
        if isinstance(value, list):
            parameters = [Argument._generate_parameter_from(inner_value, None) for inner_value in value]
            return ListParameter(parameters)
        
        if isinstance(value, dict):
            parameters = {}
            for key, inner_value in value.items():
                parameters[key] = Argument._generate_parameter_from(inner_value, None)
            return DictParameter(parameters)
        
        return ConstantParameter(value)

    def __init__(self, name, parameter):
        self._name = name
        self._parameter = parameter

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def value(self, runtime_data):
        return self._parameter.compute_value(runtime_data)

    def provenance(self):
        return {'name': self._name, 'value': self._parameter.provenance()}

    def hash(self, runtime_data):
        return self._parameter.hash(runtime_data)

    def enable_caching(self):
        self._parameter.enable_caching()

    def __str__(self):
        return self._parameter.__str__()