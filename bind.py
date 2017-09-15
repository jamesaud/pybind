
# Javascript Bind in Python
def bind(fn, *args, **kwargs):
    def inner(*new_args, **new_kwargs):
        return fn(*args, *new_args, **kwargs, **new_kwargs)
    return inner

def add(a, b):
    return a + b

add3 = bind(add, 3)
#print(add3(2))

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

print(add.bind(3)(2))


class Test:
    def method(self):
        print("TEST METHOD")

    def call(self):
        return self.method()

class Dog:
    def method(self):
        print("Dog METHOD")

method = bind(Test.call, Dog())
#method()
