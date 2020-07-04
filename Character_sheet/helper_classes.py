from helper_functions import LDK


class effect:

    # TODO: Need to be able to remove as well

    def add_effect(self, char):
        path_string = self.aspect.split(".")
        path = LDK(char, path_string)
        path[self.origin] += [self.value]


class modifier(effect):
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value


class note(effect):
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value


class feature(effect):
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value
