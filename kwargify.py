# -*- coding: utf-8 -*-
import inspect


class kwargify(object):
    def __init__(self, function):
        self._f = function
        self._defaults = {}
        self.func_defaults = tuple([])
        argspec = inspect.getargspec(self._f)
        self._args = argspec.args
        f_defaults = argspec.defaults
        if f_defaults is not None:
            for key, value in zip(self._args[-len(f_defaults):], f_defaults):
                self._defaults[key] = value

    def __call__(self, *args, **kwargs):
        pass_args = []
        if len(args) > len(self._args):
            raise TypeError(
                "Too many parameters passed! ({} passed, {} possible)".format(
                    len(args), len(self._args)))
        for arg in args:
            pass_args.append(arg)
        for arg in self._args[len(args):]:
            if arg in kwargs:
                pass_args.append(kwargs[arg])
            elif arg in self._defaults:
                pass_args.append(self._defaults[arg])
            else:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return self._f(*pass_args)

    @property
    def __name__(self):
        return self._f.__name__

    @property
    def __doc__(self):
        return self._f.__doc__

    @property
    def func_closure(self):
        return self._f.func_closure

    @property
    def func_code(self):
        return self._f.func_code

    @property
    def func_dict(self):
        return self._f.func_dict

    @property
    def func_doc(self):
        return self._f.func_doc

    @property
    def func_globals(self):
        return self._f.func_globals

    @property
    def func_name(self):
        return self._f.func_name
