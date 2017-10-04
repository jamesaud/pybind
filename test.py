

class Dog:
    def hello(self, greeting):
        print("Hello " + greeting)



d = Dog()


def call_class_with_args(obj, method_name, *args, **kwargs):
    method = getattr(obj, method_name)
    
    def inner(*a, **kw):
        return method(*args, *a, **kw, **kwargs)

    obj.__dict__[method_name] = inner
    return inner

call_class_with_args(d, 'hello', "world")
d.hello()

def update_dog(obj):

    def inner():
        obj.hello = lambda: print("updated")
    return inner

d.hello.__dict__['bind'] = update_dog(d)

print(d.hello.__dict__)
d.hello.bind()

d.hello()
