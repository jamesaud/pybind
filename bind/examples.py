from bind_functions import bindable, bind, bound
from bind_class import bindableclass
from bind_class import bindable_class_methods
from bind_instance import bindable_instance_methods
from MetaBind import BindableMeta


##### FUNCTIONS #####

def add(a, b):
    return a + b


###  'bind' allows assigning default arguments to a function ###
add3 = bind(add, 3)
print(add3(4))              # >> 7

always10 = bind(add, 3, 7)
print(always10())           # >> 10



###  'bindable' is a decorator that adds a method called '.bind' to a function  ###
@bindable
def add(a, b):
    return a + b

add3 = add.bind(3)
print(add3(5))              # >> 8


# bound allows for callbacks
@bound
def add(a, b):
    return a + b

add3 = add.bind(3)
print(add3(8))              # >> 11

add3.add_callback(lambda x: print(str(x) + " squared is: " + str(x**2)))     #  >> 11 squared is: 121
add3(8)


##### INSTANCES #####

### Bindable Instance Methods: Automatically makes user defined methods bindable to that instance with 'bind'

@bindable_instance_methods
class Dog():

    def bark(self, *args):
        print(*args)



dog = Dog()
dog.bark.bind("hi", "there")    # >> hi there
dog.bark()
dog.bark("friend!")             # >> hi there friend!




#### CLASS METHODS #####

### Bindable Class: Creates new class with '.bind' that passes default arguments to the init function

@bindableclass
class Dog():

    def __init__(self, fname, lname):
        self.name = fname + " " + lname

    def greet(self):
        print("Hello, Bark, my name is " + self.name)

    def bark(self, *args):
        """ Puts bark in between every argument passed to the function and prints it """
        print(*args)


LilDog = Dog.bind("Lil")
pup = LilDog("Pup")
pup.greet()                     # >> Hello, Bark, my name is Lil Pup


### bindable_class_methods: Creates new class with '.bind' that passes default arguments to the function called with '.bind'

@bindable_class_methods
class Dog():

    def __init__(self, fname, lname):
        self.name = fname + " " + lname

    def greet(self):
        print("Hello, Bark, my name is " + self.name)

    def bark(self, *args):
        """ Puts bark in between every argument passed to the function and prints it """
        print(*args)


FunnyDog = Dog.bark.bind("Haha")
dog = FunnyDog("Funny", "Dog")
dog.bark("You Look Nice")               # >> Haha You Look Nice



#### META CLASS #####

### BindableMeta: Makes the class have bindable_class_methods and bindable_instance_methods
###               Plus, all inherited classes are also bindable.

class Dog(metaclass=BindableMeta):

    def __init__(self, fname="", lname=""):
        self.name = fname + " " + lname

    def greet(self):
        print("Hello, Bark, my name is " + self.name)

    def bark(self, *args):
        """ Puts bark in between every argument passed to the function and prints it """
        print(*args)



Doggo = Dog.bind("Lassi")
Doggo().greet()             # >> Hello, Bark, my name is Lassi

dog = Dog()
dog.bark.bind("Hi")
dog.bark()                  # >> Hi

BarkDog = Dog.bark.bind("Woof", "Woof")    # > Woof Bark! Woof
BarkDog().bark()

class Pup(Dog):

    def pet(self, name):
        print("That feels good " + name + "!")


### Subclassed
SoloPup = Pup.pet.bind("when I pet myself")
pup = SoloPup()
pup.pet()                       # >> That feels good when I pet myself!
