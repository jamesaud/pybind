from bind_instance import bindable_instance_methods
from bind_class import bindable_class_methods

class BindableClassMeta(type):
    def __init__(cls, bases, name, dct):
        bindable_class_methods(cls)
        return super().__init__(bases, name, dct)


class BindableMethodsMeta(type):
    def __init__(cls, bases, name, dct):
        bindable_instance_methods(cls)
        return super().__init__(bases, name, dct)


class BindableMeta(BindableClassMeta, BindableMethodsMeta):
    pass
