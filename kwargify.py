# -*- coding: utf-8 -*-
import sys


def kwargify(function):
    from functools import wraps
    import inspect

    @wraps(function)
    def _wrapped(**kwargs):
        f_args = inspect.getargspec(function).args
        f_defaults = inspect.getargspec(function).defaults
        defaults = {}
        if f_defaults is not None:
            for key, value in zip(f_args[-len(f_defaults):], f_defaults):
                defaults[key] = value

        args = []
        for arg in f_args:
            if arg in kwargs:
                args.append(kwargs[arg])
            elif arg in defaults:
                args.append(defaults[arg])
            else:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return function(*args)
    return _wrapped

sys.modules[__name__] = kwargify
