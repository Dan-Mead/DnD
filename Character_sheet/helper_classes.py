from helper_functions import LDK


class effect:

    # TODO: Need to be able to remove as well

    def add_effect(self, char):
        path_string = self.aspect.split(".")
        path = LDK(char, path_string)
        path[self.origin] += [self.value]


class modifier(effect):
    """Adds a single stat, usually a single modifier"""
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value


class note(effect):
    """Add a note. Currently on saving throws and skills"""
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value


class flavour(effect):
    """Add a single effect for something that is purely a description."""
    def __init__(self, origin, aspect, value):
        self.origin = origin
        self.aspect = aspect
        self.value = value


class trigger_passive(effect):
    pass


class passive_effect(effect):
    pass


class active_effect(effect):
    pass