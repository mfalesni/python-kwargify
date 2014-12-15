# -*- coding: utf-8 -*-
import inspect


class kwargify(object):
    def __init__(self, function):
        self._f = function
        self._defaults = {}
        self._args = inspect.getargspec(self._f).args
        f_defaults = inspect.getargspec(self._f).defaults
        if f_defaults is not None:
            for key, value in zip(self._args[-len(f_defaults):], f_defaults):
                self._defaults[key] = value

    def __call__(self, **kwargs):
        args = []
        for arg in self._args:
            if arg in kwargs:
                args.append(kwargs[arg])
            elif arg in self._defaults:
                args.append(self._defaults[arg])
            else:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return self._f(*args)

    @property
    def __name__(self):
        return self._f.__name__
