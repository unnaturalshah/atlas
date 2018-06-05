class MiddlewareChain(object):

    def __init__(self):
        from logging import getLogger

        self._chain = []
        self._log = getLogger(__name__)

    def chain(self):
        return self._chain

    def append_middleware(self, middleware):
        self._chain.append(middleware)

    def extend(self, list_of_middleware):
        self._chain.extend(list_of_middleware)

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        return self._call_internal(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, 0)

    def _call_internal(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index):
        def recursive_callback(args, kwargs):
            return self._call_internal(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index + 1)

        def execute_callback(args, kwargs):
            return callback(*args, **kwargs)

        if middleware_index < len(self._chain):
            next_callback = recursive_callback
        else:
            next_callback = execute_callback

        return self._execute_middleware(
            self._chain[middleware_index], 
            upstream_result_callback, 
            filler_builder, 
            filler_kwargs, 
            args, 
            kwargs, 
            next_callback
        )

    def _execute_middleware(self, current_middleware, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, next_callback):
        log_string = 'Calling middleware {} with {}, {}, {}, {}, {}, {}'.format(
                current_middleware, 
                upstream_result_callback, 
                filler_builder, 
                filler_kwargs, 
                args, 
                kwargs, 
                next_callback
            )
        self._log.debug(log_string)
        return current_middleware.call(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, next_callback)

    def __add__(self, other):
        new_chain = MiddlewareChain()

        if isinstance(other, list):
            new_chain.extend(self.chain())
            new_chain.extend(other)
        else:
            new_chain.extend(self._chain)
            new_chain.extend(other.chain())

        return new_chain
