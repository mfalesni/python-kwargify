# -*- coding: utf-8 -*-
import sys


def kwargify(function):
    from functools import wraps
    import inspect

    @wraps(function)
    def _wrapped(**kwargs):
        args = []
        for arg in inspect.getargspec(function).args:
            try:
                args.append(kwargs[arg])
            except KeyError:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return function(*args)
    return _wrapped

sys.modules[__name__] = kwargify
