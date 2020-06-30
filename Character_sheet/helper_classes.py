from addict import Dict
from helper_functions import LDK

class Effect():

    ## TODO: Need to be able to remove as well

    def add_effect(self, char):

        path_string = self.aspect.split(".")
        path = LDK(char, path_string)
        path[self.origin] += [self.value]

class Modifier(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value
            

class Note(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value


class Feature(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value