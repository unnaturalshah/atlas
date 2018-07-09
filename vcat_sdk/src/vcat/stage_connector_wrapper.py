"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_piping import StagePiping
from vcat.job import Job
from vcat.successive_argument_filler import SuccessiveArgumentFiller
from vcat.stage_connector import StageConnector
from vcat.stage_context import StageContext
from vcat.context_aware import ContextAware

class StageConnectorWrapper(object):

    def __init__(self, connector, pipeline_context, stage_context, stage_config):
        self._connector = connector
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context
        self._stage_config = stage_config

        self._stage_context.uuid = self.uuid()
        self._pipeline_context.add_stage_context(self._stage_context)

        self._stage_piping = StagePiping(self)

    def _reset_state(self):
        self._connector._reset_state()

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._connector.uuid()

    def add_tree_names(self, **filler_kwargs):
        self._connector.add_tree_names(
            self._pipeline_context.provenance.stage_hierarchy, self._provenance_filler_builder, **filler_kwargs)

    def stage(self, function, *args, **kwargs):
        from vcat.stage_connector_wrapper_builder import StageConnectorWrapperBuilder

        builder = StageConnectorWrapperBuilder(self._pipeline_context)
        builder = builder.stage(self.uuid(), function, args, kwargs)
        builder = builder.hierarchy([self.uuid()])

        return builder.build(self._connector.stage)

    def persist(self):
        self._stage_config.persist()
        return self

    def set_global_cache_name(self, name):
        self._stage_config.cache(name)
        return self

    def enable_caching(self):
        self._stage_config.enable_caching()
        return self

    def disable_caching(self):
        self._stage_config.disable_caching()
        return self

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)

    def run(self, params_dict={}, **kw_params):
        import uuid

        from vcat.global_state import deployment_manager
        from vcat.deployment_wrapper import DeploymentWrapper

        all_params = params_dict.copy()
        all_params.update(kw_params)

        job_name = str(uuid.uuid4())
        job = Job(self, **all_params)
        deployment = deployment_manager.deploy({}, job_name, job)

        return DeploymentWrapper(deployment)

    def run_same_process(self, **filler_kwargs):
        self.add_tree_names(**filler_kwargs)
        return self.run_without_provenance(**filler_kwargs)

    def run_without_provenance(self, **filler_kwargs):
        return self._connector.run(self._filler_builder, **filler_kwargs)

    def _filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_fill import HyperparameterArgumentFill
        from vcat.stage_connector_wrapper_fill import StageConnectorWrapperFill

        return SuccessiveArgumentFiller([HyperparameterArgumentFill, StageConnectorWrapperFill], *args, **kwargs)

    def _provenance_filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_name_fill import HyperparameterArgumentNameFill
        from vcat.stage_connector_wrapper_name_fill import StageConnectorWrapperNameFill

        return SuccessiveArgumentFiller([HyperparameterArgumentNameFill, StageConnectorWrapperNameFill], *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def name(self):
        return self._connector.name()

    def splice(self, num_children):
        def splice_at(data_frames, slot_num):
            return data_frames[slot_num]

        children = []

        for child_index in range(num_children):
            child = self | (splice_at, child_index)
            children.append(child)

        return children

    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super(StageConnectorWrapper, self).__getattr__(name)

        def call_method_on_instance(instance, *args, **kwargs):
            result = getattr(instance, name)(*args, **kwargs)
            if result is None:
                return instance
            return result

        def auto_stage(*args, **kwargs):
            return self.stage(call_method_on_instance, *args, **kwargs)

        return auto_stage

    def __getitem__(self, key):
        def getitem(data, key):
            return data[key]

        return self.stage(getitem, key)

    @staticmethod
    def _generate_random_params_set(params_range_dict):
        return {key: params_range.random_sample() for key, params_range in params_range_dict.items()}

    @staticmethod
    def _create_random_params_set_generator(params_range_dict):
        while True:
            yield StageConnectorWrapper._generate_random_params_set(params_range_dict)

    def _create_and_run_param_sets(self, params_set_generator, max_iterations):
        from vcat.utils import take_from_generator

        if max_iterations is None:
            truncated_params_set_generator = params_set_generator
        else:
            truncated_params_set_generator = take_from_generator(max_iterations, params_set_generator)

        all_deployments = map(self.run, truncated_params_set_generator)
        return {deployment.job_name(): deployment for deployment in all_deployments}

    def random_search(self, params_range_dict, max_iterations):
        random_params_set_generator = StageConnectorWrapper._create_random_params_set_generator(params_range_dict)
        return self._create_and_run_param_sets(random_params_set_generator, max_iterations)

    @staticmethod
    def _create_grid_search_params_set_generator(params_range_dict):
        import itertools

        keys = list(params_range_dict.keys())
        keys.sort()
        params_grid_elements = list(map(lambda key: params_range_dict[key].grid_elements(), keys))

        if params_grid_elements != []:
            params_cartesian_product = itertools.product(*params_grid_elements)

            for params_tuple in params_cartesian_product:
                yield {key: param for key, param in zip(keys, params_tuple)}

    def grid_search(self, params_range_dict, max_iterations=None):
        grid_params_set_generator = StageConnectorWrapper._create_grid_search_params_set_generator(params_range_dict)
        return self._create_and_run_param_sets(grid_params_set_generator, max_iterations)

    def _drain_queue(self, params_queue, deployments_map, params_generator_function, error_handler):
        from vcat.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not params_queue.empty():
            params_to_run = params_queue.get()
            deployment = self.run(params_to_run)
            deployments_map[deployment.job_name()] = deployment
            log.info(deployment.job_name() + ' created')

        log.info('----------\n')

        self._check_deployments_and_populate_queue(params_queue, deployments_map, params_generator_function, error_handler)

    @staticmethod
    def _populate_queue(params_queue, set_of_initial_params):
        for initial_params in set_of_initial_params:
            params_queue.put(initial_params)

    def _check_deployments_and_populate_queue(self, params_queue, deployments_map, params_generator_function, error_handler):
        import time

        from vcat.global_state import log_manager
        from vcat.deployment_utils import _collect_results_and_remove_finished_deployments

        log = log_manager.get_logger(__name__)

        if deployments_map != {}:
            all_logged_results = _collect_results_and_remove_finished_deployments(deployments_map, error_handler)

            for logged_results in all_logged_results:
                new_params_sets = params_generator_function(logged_results)
                StageConnectorWrapper._populate_queue(params_queue, new_params_sets)

            if all_logged_results != []:
                self._drain_queue(params_queue, deployments_map, params_generator_function, error_handler)
            else:
                time.sleep(5)
                self._populate_queue(params_queue, deployments_map, params_generator_function, error_handler)
        else:
            log.info('Adaptive search completed.')

    def adaptive_search(self, set_of_initial_params, params_generator_function, error_handler=None):
        from vcat.compat import make_queue

        params_queue = make_queue()
        deployments_map = {}

        StageConnectorWrapper._populate_queue(params_queue, set_of_initial_params)

        self._drain_queue(params_queue, deployments_map, params_generator_function, error_handler)