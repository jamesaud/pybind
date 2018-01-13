from MetaBind import BindableMeta, BindableMethodsMeta

# class Dog(metaclass=BindableMeta):
#
#     def __init__(self, name):
#         self.name = name
#
#     def greet(self, optional=""):
#         return f"Bark, my name is {self.name}, {optional}"
#
#
# #Dog(name="hello")
# #Greet_Dog = Dog.greet.bind("I'm a Dog")
# #Greet_Dog("Spade").greet()


class Cat(metaclass=BindableMeta):

    def __init__(self, name):
        self.name = name

    def greet(self, optional=""):
        return f"Bark, my name is {self.name}, {optional}"

GreetCat = Cat.greet.bind("hello")
print(GreetCat("Kirst").greet())
print(Cat("Kirst").greet("ah"))