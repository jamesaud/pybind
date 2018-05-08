from bind_class import bindableclass, bindable_class_methods


# Bindable Class: Creates new class with '.bind' that passes default arguments to the init function

@bindableclass
class Dog():
    def __init__(self, fname, lname):
        self.name = fname + " " + lname

    def bark(self, *args):
        print(*args)

    def greet(self):
        print("Hello, Bark, my name is " + self.name)


LilDog = Dog.bind("Lil")
pup = LilDog("Pup")
pup.greet()                     # >> Hello, Bark, my name is Lil Pup


# bindable_class_methods: Creates new class with '.bind' that passes default arguments to the function called with '.bind'

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

