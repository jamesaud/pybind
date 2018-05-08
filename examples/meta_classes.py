from MetaBind import BindableMeta


# BindableMeta: Makes the class have bindable_class_methods and bindable_instance_methods
#               Plus, all inherited classes are also bindable.

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
