
# Javascript Bind in Python
def bind(fn, *args, **kwargs):
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
        def inner(*new_args, **new_kwargs):
            return fn(*args, *new_args, **kwargs, **new_kwargs)
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
print(add.bind(3)(2))


class Test:
    def method(self):
        print("TEST METHOD")

    def call(self):
        return self.method()

class Dog:
    def method(self):
        print("Dog METHOD")


print("\nBIND 3")
method = bind(Test.call, Dog())
method()



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

print("BIND 4")
print(b())


    
