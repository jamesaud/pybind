from MetaBind import BindableMeta


# BindableMeta: Makes the class have bindable_class_methods and bindable_instance_methods
#               Plus, all inherited classes are also bindable.

class Dog(metaclass=BindableMeta):
    def __init__(self, fname="", lname=""):
        self.name = fname + " " + lname

    def greet(self):
        print("Hello, Bark, my name is " + self.name)

    def bark(self, *args):
        print(*args)


# Bind class
Doggo = Dog.bind("Lassi")
Doggo().greet()  # >> Hello, Bark, my name is Lassi

# Bind instance
dog = Dog()
dog.bark.bind("Hi")
dog.bark()  # >> Hi

# Bind class method
BarkDog = Dog.bark.bind("Woof", "Woof")
BarkDog().bark()  # > Woof Woof


# Subclass
class Pup(Dog):
    def pet(self, name):
        print("That feels good " + name + "!")


SoloPup = Pup.pet.bind("when I pet myself")
pup = SoloPup()
pup.pet()  # >> That feels good when I pet myself!