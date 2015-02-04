# -*- coding: utf-8 -*-
import inspect


def kwargify(wrapped):
    _method = hasattr(wrapped, "im_func") or type(wrapped).__name__ == "method"
    _defaults = {}
    argspec = inspect.getargspec(wrapped)
    if _method:
        _args = argspec.args[1:]
    else:
        _args = argspec.args
    f_defaults = argspec.defaults
    if f_defaults is not None:
        for key, value in zip(_args[-len(f_defaults):], f_defaults):
            _defaults[key] = value

    def wrapper(*args, **kwargs):
        pass_args = []
        if len(args) > len(_args):
            raise TypeError(
                "Too many parameters passed! ({} passed, {} possible)".format(
                    len(args), len(_args)))
        for arg in args:
            pass_args.append(arg)
        for arg in _args[len(args):]:
            if arg in kwargs:
                pass_args.append(kwargs[arg])
            elif arg in _defaults:
                pass_args.append(_defaults[arg])
            else:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return wrapped(*pass_args)

    # Doing the work of functools.wraps from python 3.2+
    assigned = ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    vars(wrapper).update(vars(wrapped))
    wrapper.__wrapped__ = wrapped
    return wrapper
