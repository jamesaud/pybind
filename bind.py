from functools import wraps
from collections import namedtuple
import inspect
import types

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


def add(a, b):
    return a + b

add3 = bind(add, 3)
print("\nBIND 1:")
print(add3(2))

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


@bindable
def add(a, b):
    return a + b

print("\nBIND 2:")
print(add.bind(3)(5))


"""
 CLASS BINDING DECORATORS:
 Decorators that bind methods of the CLASS to generate a new, identical class with the bound methods
"""


# UTILITIES
def clone_class(cls):
    # Recreate the class
    return type(cls.__name__, cls.__bases__, dict(cls.__dict__))

def method_is_classmethod(cls, method_name):
    return isinstance(inspect.getattr_static(cls, method_name), classmethod)

def method_is_staticmethod(cls, method_name):
    return isinstance(inspect.getattr_static(cls, method_name), staticmethod)

def isBuiltIn(name):
    return True if (name.startswith("__") and name.endswith("__")) else False

def get_user_defined_methods(cls):
    return [method_name for method_name in dir(cls) if callable(getattr(cls, method_name)) and
     not isBuiltIn(method_name)]


def bind_self_last(obj, method_name, *args, **kwargs):
    """ Binds a method, allowsing self to be passed when the method is called """
    method = getattr(obj, method_name)

    @wraps(method)
    def pass_self_last(self, *a, **kw):
        """ Passes 'self' as the first argument """
        return method(self, *args, *a, **kwargs, **kw)

    return pass_self_last


def create_class_with_bound_method(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters *args and **kwargs """
    method = getattr(cls, method_name)

    wrapper_cls = clone_class(cls)
    setattr(wrapper_cls, method_name, bind_self_last(cls, method_name, *args, **kwargs))
    return wrapper_cls


def create_class_with_bound_staticmethod(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters"""
    wrapper_cls = clone_class(cls)
    setattr(wrapper_cls, method_name, bind(getattr(cls, method_name), *args, **kwargs))
    return wrapper_cls


def bindclass(cls, *args, **kwargs):
    """ Generates new class where the __init__ function of the class has default parameters """
    return create_class_with_bound_method(cls, "__init__", *args, **kwargs)


def bindableclass(cls):
    # A class with the function .bind() added onto it
    cls.bind = bind(create_class_with_bound_method, cls, "__init__")
    return cls


def _make_bindable_method(cls, method_name):
    method = getattr(cls, method_name)
    # method.bind() will return a new class based on the method's current class
    method.bind = bind(create_class_with_bound_method, cls, method_name)
    return method


def _make_bindable_staticmethod(cls, method_name):
    method = getattr(cls, method_name)
    method.bind = bind(create_class_with_bound_staticmethod, cls, method_name)
    return method


# Decorator
def bindablemethods(cls):
    cls = bindableclass(cls)
    method_list = get_user_defined_methods(cls)

    # Give all user defined methods a ".bind()" method
    for method_name in method_list:
        if method_is_classmethod(cls, method_name):
            pass

        elif method_is_staticmethod(cls, method_name):
            _make_bindable_staticmethod(cls, method_name)

        else:
            _make_bindable_method(cls, method_name)

    # Return the new class
    return cls


# TODO make bind work with @classmethods
# TODO make @bindablemethods work on object that instantiates
# TODO make @bindableclass
# TODO make @bindableinit
# TODO make @bindableinstancemethods

@bindablemethods
class Quack:
    def hello(self, y):
        print("hello " + y)

    @classmethod
    def world(cls):
        print("WORLD")

    @staticmethod
    def awesome(x):
        print("AWESOME " + x)


print("\nBind All Class Methods")
NewQuack = Quack.hello.bind("world")  # should be a new class
NewQuack().hello()

NewQuack = Quack.awesome.bind("a")
NewQuack.awesome()

@bindableclass
class Duck:
    def __init__(self, x, y="hey", z="world"):
        print("Calling x with " + str(x) + y + z)


print("\nBIND 4")
bound_duck = bindclass(Duck, 3)
bound_duck = bindclass(bound_duck, "my")
print("Hi, I'm a clone of " + bound_duck.__name__)
bound_duck("god")

bound_duck = Duck.bind(4)
print("\nHi, I'm a clone of " + bound_duck.__name__)
bound_duck()


"""
 INSTANCE BINDING DECORATORS:
 Decorators that bind methods of the INSTANCE to update the INSTANCE with the bound methods
"""

def bind_instance_method(obj, method_name, *args, **kwargs):
    """ Binds a method on the instance of a class """
    method = getattr(obj, method_name)
    return method

class Muck:

    def hello(self, greeting):
        print("hello " + greeting)

m = Muck()
print("\n--- BIND INSTANCE METHOD ---")
bind_instance_method(m, "hello", "world")





"""
 Function BINDING Class:
 Class to wrap a function and bind it.
"""

class Bound:

    def __init__(self, fn, *args, **kwargs):
        self.fn = self.__bind(fn, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __bind(self, fn, *args, **kwargs):
        return lambda *a, **kw: fn(*args, *a, **kwargs, **kw)

    def __callback(self, fn, fn2):
        @wraps(fn)
        def callback(*args, **kwargs):
            result = fn(*args, **kwargs)
            return fn2(result)

        return callback

    def bind(self, *args, **kwargs):
        self.fn = self.__bind(self.fn, *args, **kwargs)
        return self

    def add_callback(self, fn):
        self.fn = self.__callback(self.fn, fn)
        return self


b = Bound(add, 3)
b.bind(20)
print("\nBIND 5")
print(b())

print("\nBIND 6")
b.add_callback(str).add_callback(lambda x: x*3)
print(b())


# META CLASS VERSION TO BIND INSTANCE METHODS
print("\n--- Meta ---")

class MyMetaTitle(type):
    def __new__(cls, name, parents, dct):
        # Makes every attribute a title
        dct = {(name.title() if not isBuiltIn(name) else name): val for name, val in dct.items()}
        return super().__new__(cls, name, parents, dct)



