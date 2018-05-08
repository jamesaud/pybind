from bind_instance import bindable_instance_methods


# Bindable Instance Methods: Automatically makes user defined methods bindable to that instance with 'bind'

@bindable_instance_methods
class Dog():

    def bark(self, *args):
        print(*args)



dog = Dog()
dog.bark.bind("hi", "there")    # >> hi there
dog.bark()
dog.bark("friend!")             # >> hi there friend!

