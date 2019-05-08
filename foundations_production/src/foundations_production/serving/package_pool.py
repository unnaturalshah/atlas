"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class PackagePool(object):
    def __init__(self, active_package_limit):
        self._model_packages = {}

    def add_package(self, model_id):
        from foundations_production.serving.restartable_process import RestartableProcess
        from foundations_production.serving.package_runner import run_model_package

        pipe = RestartableProcess(target=run_model_package, args=(model_id))
        self._model_packages[model_id] = pipe

    def run_prediction_on_package(self, model_id, data):
        self._model_packages[model_id].send(data)
