from bind_functions import *

"""
 CLASS BINDING DECORATORS:
 Decorators that bind methods of the CLASS to generate a new, identical class with the bound methods
"""


def bind_self_last(obj, method_name, *args, **kwargs):
    """ Binds a method, allowing self to be passed when the method is called """
    method = getattr(obj, method_name)

    @wraps(method)
    def pass_self_last(self, *a, **kw):
        """ Passes 'self' as the first argument """
        return method(self, *args, *a, **kwargs, **kw)

    return pass_self_last


def create_class_with_bound_instancemethod(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters *args and **kwargs """
    wrapper_cls = subclass(cls)
    setattr(wrapper_cls, method_name, bind_self_last(cls, method_name, *args, **kwargs))
    return wrapper_cls


def create_class_with_bound_staticmethod(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters"""
    wrapper_cls = subclass(cls)
    setattr(wrapper_cls, method_name, bind(getattr(cls, method_name), *args, **kwargs))
    return wrapper_cls


def create_class_with_bound_classmethod(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters"""
    wrapper_cls = subclass(cls)
    setattr(wrapper_cls, method_name, bind(getattr(cls, method_name), *args, **kwargs))
    return wrapper_cls


def bindclass(cls, *args, **kwargs):
    """ Generates new class where the __init__ function of the class has default parameters """
    return create_class_with_bound_instancemethod(cls, "__init__", *args, **kwargs)


def bindableclass(cls):
    # A class with the function .bind() added onto it
    cls.bind = bind(create_class_with_bound_instancemethod, cls, "__init__")
    return cls


# Decorator
def bindable_class_methods(cls):
    cls = bindableclass(cls)
    method_list = get_user_defined_methods(cls)

    # Give all user defined methods a ".bind()" method
    for method_name in method_list:

        if method_is_classmethod(cls, method_name):
            bind_method = bind(create_class_with_bound_classmethod, cls, method_name)

        elif method_is_staticmethod(cls, method_name):
            bind_method = bind(create_class_with_bound_staticmethod, cls, method_name)

        else:
            bind_method = bind(create_class_with_bound_instancemethod, cls, method_name)

        getattr(cls, method_name).__dict__['bind'] = bind_method    # add bind to method

    return cls


def unbind_class_methods(cls):

    if 'bind' in cls.__dict__ and callable(cls.__dict__['bind']):
        delattr(cls, 'bind')

    for method_name in get_user_defined_methods(cls):
        method = getattr(cls, method_name)
        if 'bind' in method.__dict__ and callable(method):
            del method.__dict__['bind']   # add bind to method

    return cls



