from bind_functions import bindable, bind, bound, callback


def add(a, b):
    return a + b


#  'bind' allows assigning default arguments to a function ###

add3 = bind(add, 3)
print(add3(4))              # >> 7

always10 = bind(add, 3, 7)
print(always10())           # >> 10



#  'bindable' is a decorator that adds a method called '.bind' to a function  ###

@bindable
def add(a, b):
    return a + b

add3 = add.bind(3)
print(add3(5))              # >> 8



# 'bound' allows for callbacks

@bound
def add(a, b):
    return a + b

add3 = add.bind(3)
print(add3(8))              # >> 11


# callbacks
@callback
def add(a, b):
    return a + b

add3.add_callback(lambda x: print(str(x) + " squared is: " + str(x**2)))     #  >> 11 squared is: 121
add3(8)

