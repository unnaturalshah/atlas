class TimeStageMiddleware(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        def timed_callback():
            return callback(args, kwargs)

        return self._stage_context.time_callback(timed_callback)