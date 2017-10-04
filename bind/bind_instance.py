from utilities import *
from bind_functions import *


"""
 INSTANCE BINDING DECORATORS:
 Decorators that bind methods of the INSTANCE to update the INSTANCE with the bound methods
"""


def bind_instance_method(obj, method_name, *args, **kwargs):
    """ Updates a method on an object with bound parameters """
    method = getattr(obj, method_name)
    setattr(obj, method_name, bind(method, *args, **kwargs))
    return method



def bind_instance_methods(obj):
    methods = get_user_defined_methods(obj)
    for method_name in methods:
        method = bind(getattr(obj, method_name)) # wrap function in a lambda, to prevent modifying the original Class's function
        method.__dict__['bind'] = bind(bind_instance_method, obj, method_name)
        obj.__dict__[method_name] = method
    return obj


# decorator
def bindable_instance_methods(cls):
    new = cls.__new__

    def bind_methods(*args, **kwargs):
        obj = new(*args, **kwargs)
        bind_instance_methods(obj)
        return obj

    cls.__new__ = bind_methods
    return cls


