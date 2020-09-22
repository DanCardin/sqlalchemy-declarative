import functools


class maybe_classmethod:
    """Perform as a method on instances, or instantiate an instance on classes.
    """

    def __init__(self, _method=None, **kwargs):
        self.method = _method
        self.kwargs = kwargs

    def __call__(self, method):
        self.method = method
        return self

    def __get__(self, instance, cls):
        if not instance:
            instance = cls(**self.kwargs)

        @functools.wraps(self.method)
        def decorator(*args, **kwargs):
            return self.method(instance, *args, **kwargs)

        return decorator
