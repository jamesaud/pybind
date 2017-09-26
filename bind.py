from functools import wraps

# Javascript Bind in Python
def bind(fn, *args, **kwargs):
    @wraps(fn)
    def inner(*new_args, **new_kwargs):
        return fn(*args, *new_args, **kwargs, **new_kwargs)
    return inner

def add(a, b):
    return a + b

add3 = bind(add, 3)
print("\nBIND 1:")
print(add3(2))

def bindable(fn):
    def binde(*args, **kwargs):
        @wraps(fn)
        def inner(*new_args, **new_kwargs):
            return fn(*args, *new_args, **kwargs, **new_kwargs)
        return inner
    fn.bind = binde
    return fn


# Hmm, binde looks extremely similar to bind...
def bindable(fn):
    if hasattr(fn, "bind"): raise AttributeError("'bind' is already defined")
    fn.bind = bind(bind, fn)
    return fn


@bindable
def add(a, b):
    return a + b

print("\nBIND 2:")
print(add.bind(3)(5))


class Test:
    def method(self):
        print("TEST METHOD")

    def call(self):
        return self.method()

class Dog:
    def method(self):
        print("Dog METHOD")


print("\nBIND 3")
dog = Dog()
method = bind(Test.call, dog)
method()


def bindclass(cls, **kwargs):
    # can't take normal args, because 'this' is the first arg
    wrapper_cls = type(cls.__name__, (cls,), {})
    wrapper_cls.__init__ = bind(cls.__init__, **kwargs)
    return wrapper_cls

def bindableclass(cls):
    if hasattr(cls, "bind"): raise AttributeError("'bind' is already defined")
    cls.bind = bind(bindclass, cls)
    return cls

@bindableclass
class Duck:
    y = 2
    def __init__(self, x):
        print("Calling x with " + str(x))

   # Will fail becoming @bindable class if 'bind' is defined
   # def bind():
   #     pass
        
print("\nBIND 4")
bound_duck = bindclass(Duck, x=3)
print("Hi, I'm a clone of " + bound_duck.__name__)
bound_duck()

bound_duck = Duck.bind(x=4)
print("\nHi, I'm a clone of " + bound_duck.__name__)
bound_duck()

class Bound:

    def __init__(self, fn, *a, **k):
        self.fn = self.__bind(fn, *a, **k)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __bind(self, fn, *a, **k):
        return lambda *n_a, **n_k: fn(*a, *n_a, **k, **n_k)
        
    def bind(self, *args, **kwargs):
        self.fn = self.__bind(self.fn, *args, **kwargs)

        
b = Bound(add, 3)
b.bind(20)

print("\nBIND 5")
print(b())


    
