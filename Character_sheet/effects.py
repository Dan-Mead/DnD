from helper_functions import LDK

"""Effects 


All features have effects. Are added by classes, races, or backgrounds.
Feats are basically identical to Features. 
Effects can have other origins. 
Some feats simply produce

Effects
* Modifier - Stat effects or changes.
* Notes - Conditional modifiers for skills and saving throws.
* Action - An effect that is manually activated, can be in or out of combat. 
Can have limited uses.
    * Optional actions. Can list when checking available actions.
* Triggered Effect - An effect that triggers automatically on an event.
    * These will still be optional, but heavily recommended.
* Passive Effect - An ongoing, constant effect, or one which has no specific
 trigger, or general flavour."""

class effect:

    def __init__(self, origin, aspect):
        self.origin = origin
        self.aspect = aspect


    def add_effect(self, char):
        path_string = self.aspect.split(".")
        path = LDK(char, path_string)

        if isinstance(self, modifier):
            value = self.value
        else:
            value = self.desc
        path[self.origin] += [value]



class modifier(effect):
    """Adds a single stat, usually a single modifier"""
    def __init__(self, origin, aspect, value):
        self.value = value
        super().__init__(origin, aspect)


class note(effect):
    """Add a note. Currently on saving throws and skills"""
    def __init__(self, origin, aspect, desc):
        self.desc = desc
        super().__init__(origin, aspect)


class passive_effect(effect):
    """Add a single effect for something that is purely a description."""
    def __init__(self, origin, aspect, desc):
        self.desc = desc
        super().__init__(origin, aspect)


class trigger_passive(effect):
    """Add a single effect which can be triggered by a notable event."""
    def __init__(self, origin, aspect, desc, trigger, limit):
        self.desc = desc
        super().__init__(origin, aspect)
        # TODO: Finish this!


class action(effect):
    """Adds an action and type"""
    def __init__(self, origin, aspect, desc):
        self.desc = desc
        super().__init__(origin, aspect)
        # TODO: Finish this