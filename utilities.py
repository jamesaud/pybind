import inspect
import copy


# UTILITIES

def subclass(cls):
    return type(cls.__name__ + ".", (cls,), {}) # unique namespace

def get_user_defined_attrs(cls):
    return {attr_name: copy.deepcopy(getattr(cls, attr_name)) for attr_name in dir(cls) if not isBuiltIn(attr_name)}

def method_is_classmethod(cls, method_name):
    return isinstance(inspect.getattr_static(cls, method_name), classmethod)

def method_is_staticmethod(cls, method_name):
    return isinstance(inspect.getattr_static(cls, method_name), staticmethod)

def isBuiltIn(name):
    return name.startswith("__") and name.endswith("__")

def get_user_defined_methods(cls):
    return [method_name for method_name in dir(cls) if callable(getattr(cls, method_name)) and
     not isBuiltIn(method_name)]

def add_attr_to_bound_method(obj, method_name, attr_name, attr):
    method = getattr(obj, method_name)
    method.__dict__[attr_name] = attr
    return method

def add_attrs_to_method(obj, method_name, **kwargs):
    method = getattr(obj, method_name)
    method.__dict__.update(kwargs)
    return method
