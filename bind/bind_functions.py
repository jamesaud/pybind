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

def add(a, b):
    return a + b

@bindable
def add(a, b):
    return a + b


