"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class APIFilterMixin(object):

    def _is_valid_column(self, result, column_name):
        return hasattr(result[0], column_name)

    def _get_parser(self, column_name):
        from foundations_rest_api.filters.parsers import get_parser

        return get_parser(column_name)
