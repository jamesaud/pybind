from functools import wraps

#### FUNCTION BINDING DECORATORS

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


class Cat:
    def method(self):
        print("TEST METHOD")

    def call(self):
        return self.method()

class Dog:
    def method(self):
        print("Dog METHOD")


print("\nBIND 3")
dog = Cat()
cat = Cat()
cat.call = bind(Cat.call, dog)
cat.call()


#### CLASS BINDING DECORATORS

def _gen_subclass(cls):
    return type(cls.__name__, (cls,), {})

def _bindedclassmethod(cls, method_name, *args, **kwargs):
    """ Passes 'self' as the first parameter to a class function, allowing for binding of values -
        otherwise the user may bind values to the 'self' parameter that aren't actually an instance. """
    @wraps(getattr(cls, method_name))
    def bind_method(self, *a, **kw):
        return bind(getattr(cls, method_name), self, *args, *a, **kwargs, **kw)()
    
    return bind_method

def _bindmethodtonewclass(cls, method_name, *args, **kwargs):
    """ Creates a new class, with the given method bound with parameters"""
    wrapper_cls = _gen_subclass(cls)
    setattr(wrapper_cls, method_name, _bindedclassmethod(cls, method_name, *args, **kwargs))
    return wrapper_cls

def bindclass(cls, *args, **kwargs):
    """ Generates new class where the __init__ function of the class has default parameters """
    ## _bindmethodtonewclass  functions like the below two lines
    
    # wrapper_cls = _gen_subclass(cls)
    # wrapper_cls.__init__ = _bindedclassmethod(cls, "__init__", *args, **kwargs)
    return _bindmethodtonewclass(cls, "__init__", *args, **kwargs)

def bindableclass(cls):
    if hasattr(cls, "bind"): raise AttributeError("'bind' is already defined in " + cls.__name__)
    cls.bind = bind(bindclass, cls)
    return cls

def _makebindableclassmethod(cls, method_name):
    method = getattr(cls, method_name)

    # method.bind() will return a new class based on the method's current class
    # bind is the same as:   lambda *a, **kw: _bindmethodtonewclass(cls, method_name, *a, **kw)
    method.bind = bind(_bindmethodtonewclass, cls, method_name)
    return method

def isBuiltIn(method_name):
    return True if (method_name.startswith("__") and method_name.endswith("__")) else False

def bindableclassmethods(cls):
    cls = bindableclass(cls)
    # Remove methods that can't be properly bound to create a new class with
    method_list = [method_name for method_name in dir(cls) if callable(getattr(cls, method_name)) and
                   not isBuiltIn(method_name)]
        
    # Give all user defined methods a ".bind()" method
    for method_name in method_list:
        _makebindableclassmethod(cls, method_name)

    # Return the new class
    return cls

# TODO make @classmethod and @staticmethod bindable with the above function

@bindableclassmethods
class Quack:
    def hello(self, y):
        print("hello " + y)

print("\nBind All Class Methods")
NewQuack = Quack.hello.bind("world")  # should technically be a new class
NewQuack().hello()

                
@bindableclass
class Duck:
    def __init__(self, x, y="hey", z="world"):
        print("Calling x with " + str(x) + y + z)
        
   # Will fail becoming @bindable class if 'bind' is defined
   # def bind():
   #     pass
        
print("\nBIND 4")
bound_duck = bindclass(Duck, 3)
bound_duck = bindclass(bound_duck, "my")
print("Hi, I'm a clone of " + bound_duck.__name__)
bound_duck("god")

bound_duck = Duck.bind(4)
print("\nHi, I'm a clone of " + bound_duck.__name__)
bound_duck()


### ENCAPSULATED FUNCTION BINDING

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
    
    def __init__(cls, name, bases, dct):
        print("meta init")
        return super().__init__(name, bases, dct)

    def __new__(cls, name, parents, dct):
        dct = {(name.title() if not isBuiltIn(name) else name): val for name, val in dct.items()}
        cls = super().__new__(cls, name, parents, dct)
        return cls

class MetaCache(type):

    def __init__(cls, name, parents, dct):
        objects = set()
        
        @wraps(cls.__init__)
        def AddObjectsToSet(init_function, self, *args, **kwargs):
            nonlocal objects
            obj = init_function(self, *args, **kwargs)
            if obj in objects:
                obj = objects.get(obj)        
            else:
                objects.add(self)

            return obj
            
        cls.__init__ = bind(AddObjectsToSet, cls.__init__)
        cls.get_objs = staticmethod(lambda: objects)
        
        return super().__init__(name, parents, dct)

    def __new__(cls, name, parents, dct):
        if "__eq__" not in dct: raise AttributeError("Missing '__eq__' in " + name)
        if "__hash__" not in dct: raise AttributeError("Missing '__hash__' in " + name)
        return super().__new__(cls, name, parents, dct)

    
class MyMetaDuck(metaclass=MetaCache):
    def __init__(self, name="tony"):
        self.name = name
    
    def hello(self, x="world"):
        print("hello " + str(x))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class MyMetaDog(metaclass=MetaCache):
    def __init__(self, name="bony"):
        self.name = name
    
    def hello(self, x="world"):
        print("hello " + str(x))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


duck = MyMetaDuck("Bran")
print(MyMetaDuck.get_objs())

dog = MyMetaDog("Tommy")
print(MyMetaDog.get_objs())
