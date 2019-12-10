"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ArgumentNamer(object):

    def __init__(self, function, arguments, keyword_arguments):
        self._function = function

        if hasattr(self._function, '__self__'):
            self._arguments = (self._function.__self__,) + arguments
        else:
            self._arguments = arguments
        self._keyword_arguments = keyword_arguments
    
    def name_arguments(self):
        try:
            from inspect import getfullargspec as getargspec
        except ImportError:
            from inspect import getargspec

        result = []
        argument_index = 0

        argspec = getargspec(self._function)
        filled_arguments = set()

        defaults = self._get_function_defaults(argspec)

        for argument_name in argspec.args:
            if argument_name in self._keyword_arguments:
                result.append((argument_name, self._keyword_arguments[argument_name]))
            elif argument_index < len(self._arguments):
                result.append((argument_name, self._arguments[argument_index]))
                argument_index += 1
            elif defaults.get(argument_name, False):
                result.append((argument_name, defaults[argument_name]))
            filled_arguments.add(argument_name)

        while argument_index < len(self._arguments):
            result.append(('<args>', self._arguments[argument_index]))
            argument_index += 1

        for key, value in self._keyword_arguments.items():
            if key not in filled_arguments:
                result.append((key, value))

        return result

    def _get_function_defaults(self, argspec):
        defaults = {}
        if argspec.defaults:
            for default_argument_index in range(len(argspec.defaults)):
                reverse_index = -default_argument_index - 1
                defaults[argspec.args[reverse_index]] = argspec.defaults[reverse_index]
        return defaults