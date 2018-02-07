from utilities import *
from functools import wraps

"""
 FUNCTION BINDING DECORATORS:
 Decorators that bind methods of functions to generate a new, identical functions with the bound variables
"""
# Javascript Bind in Python
def bind(fn, *args, **kwargs):
    @wraps(fn)
    def inner(*a, **kw):
        return fn(*args, *a, **kwargs, **kw)
    return inner


def bindable(fn):
    def binde(*args, **kwargs):
        @wraps(fn)
        def inner(*a, **kw):
            return fn(*args, *a, **kwargs, **kw)
        return inner
    fn.bind = binde
    return fn


# Hmm, binde looks extremely similar to bind...
def bindable(fn):
    fn.bind = bind(bind, fn)
    return fn




 # Class to wrap a function and bind it.
class bound:

    def __init__(self, fn, *args, **kwargs):
        self.fn = self.__bind(fn, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __bind(self, fn, *args, **kwargs):
        return lambda *a, **kw: fn(*args, *a, **kwargs, **kw)

    def __callback(self, fn, fn2):
        @wraps(fn)
        def callback(*args, **kwargs):
            results = fn(*args, **kwargs)
            return fn2(fn(*args, **kwargs))

        return callback

    def bind(self, *args, **kwargs):
        self.fn = self.__bind(self.fn, *args, **kwargs)
        return self

    def add_callback(self, fn):
        self.fn = self.__callback(self.fn, fn)
        return self


