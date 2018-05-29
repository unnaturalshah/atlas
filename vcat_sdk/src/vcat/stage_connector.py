class StageConnector(object):

    def __init__(self, current_stage, previous_connectors):
        self.current_stage = current_stage
        self._previous_connectors = previous_connectors
        self._has_run = False
        self._result = None

    def _reset_state(self):
        self._has_run = False
        self._result = None

        for previous_connector in self._previous_connectors:
            previous_connector._reset_state()

    def name(self):
        return self.current_stage.name()

    def function_name(self):
        return self.current_stage.function_name()

    def args(self):
        return self.current_stage.args

    def kwargs(self):
        return self.current_stage.kwargs

    def add_tree_names(self, stages_dict, filler_builder, **filler_kwargs):
        parent_ids = [connector.add_tree_names(
            stages_dict, filler_builder, **filler_kwargs) for connector in self._previous_connectors]
        filler = filler_builder(*self.args(), **self.kwargs())
        args, kwargs = filler.fill(**filler_kwargs)
        this_stage = {"function_name": self.function_name(
        ), "args": args, "kwargs": kwargs, "parents": parent_ids}
        stages_dict[self.name()] = this_stage
        return self.name()

    def stage(self, next_stage):
        return StageConnector(next_stage, [self])

    def run(self, filler_builder, **filler_kwargs):
        if self._has_run:
            return self._result
        else:
            previous_results = [connector.run(
                filler_builder, **filler_kwargs) for connector in self._previous_connectors]
            self._result = self.current_stage.run(
                previous_results, filler_builder, **filler_kwargs)
            self._has_run = True
            return self._result