"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import ValidationReportListingsController

class TestValidationReportListingsController(Spec):

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_package(self):
        return self.faker.word()

    @let
    def data_contract(self):
        return self.faker.word()

    @let
    def inference_period(self):
        return self.faker.date()

    @let
    def model_package_2(self):
        return self.faker.word()

    @let
    def data_contract_2(self):
        return self.faker.word()

    @let
    def inference_period_2(self):
        return self.faker.date()

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def controller(self):
        return ValidationReportListingsController()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()
        self.controller.params = {'project_name': self.project_name}

    def test_index_returns_empty_list_as_response_if_no_reports_in_redis(self):
        self.assertEqual([], self.controller.index().as_json())

    def test_index_returns_resource_with_resource_name_validation_report_listings(self):
        result = self.controller.index()
        self.assertEqual('ValidationReportListings', result.resource_name())

    def test_index_returns_list_with_one_listing_if_exists_in_redis(self):
        self._register_report(self.project_name, self.model_package, self.data_contract, self.inference_period)
        result = self.controller.index()

        expected_result = [
            {
                "data_contract": self.data_contract,
                "model_package": self.model_package,
                "inference_period": self.inference_period
            }
        ]

        self.assertEqual(expected_result, result.as_json())

    @staticmethod
    def _key_to_write(project_name, model_package, data_contract):
        return f'projects:{project_name}:models:{model_package}:validation:{data_contract}'

    def _register_report(self, project_name, model_package, data_contract, inference_period):
        key_to_write = self._key_to_write(project_name, model_package, data_contract)
        self.redis_connection.hset(key_to_write, inference_period, 'dummy_report')