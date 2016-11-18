# -*- coding: utf-8 -*-
import functools


class reprwrapper(object):
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kw):
        return self._func(*args, **kw)

    def __repr__(self):
        return self._repr(self._func)


def withrepr(reprfun):
    """Use: @withrepr(lambda x: "<Func: %s>" % x.__name__)
    :param reprfun:
    :return:
    """
    def _wrap(func):
        return reprwrapper(reprfun, func)
    return _wrap


def catch(fn):
    def fn2(*args, **kwargs):
        exceptions = kwargs.pop('exceptions', (Exception,))
        return_value = kwargs.pop('return_value', None)
        try:
            return fn(*args, **kwargs)
        except exceptions:
            return return_value
    return fn2