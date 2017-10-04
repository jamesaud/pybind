
from MetaBind import BindableMeta
# BindNewMeta


class Dog(metaclass=BindableMeta):
    a = []

    def hello(self, *args):
        print("hello " + str([arg for arg in args]))



