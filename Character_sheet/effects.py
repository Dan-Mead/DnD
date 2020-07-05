from helper_functions import LDK

"""Effects 


All features have effects. Are added by classes, races, or backgrounds.
Feats are basically identical to Features. 
Effects can have other origins. 
Some feats simply produce

Effects
* Notes - Conditional modifiers for skills and saving throws.
* Modifier - Stat effects or changes.
* Action - An effect that is manually activated, can be in or out of combat
. Can have limited uses.
    * Optional actions. Can list when checking available actions.
* Triggered Effect - An effect that triggers automatically on an event.
    * These will still be optional, but heavily recommended.
* Passive Effect - An ongoing, constant effect, or one which has no specific
 trigger, or general flavour."""

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