import inspect
import sys

from effects import passive_effect, trigger_passive, action

def get_features():
    features = {}
    for feature_name, feature_object in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if sys.modules[__name__].feature in feature_object.__mro__ and not feature_object.__subclasses__():
            features[feature_name.replace("_", " ")] = feature_object

    return features


def get_feature(feature_name):
    features = get_features()

    return features[feature_name]


class feature:
    pass



class Darkvision(feature, passive_effect):
    def __init__(self, origin):
        desc = 'You can see in dim light within 60 feet of you as if it ' \
                    'were bright light, and in darkness as if it were dim ' \
                    'light. You can’t discern color in darkness, only shades ' \
                    'of gray. '
        passive_effect.__init__(self, origin, "features", desc)



class Relentless_Endurance(feature, trigger_passive):
    def __init__(self, origin):
        desc = 'When you are reduced to 0 Hit Points but not killed ' \
                    'outright, you can drop to 1 hit point instead. You can’t ' \
                    'use this feature again until you finish a Long Rest. '
        trigger = ["Zero HP"]
        limit = {'num' : 1,
                 'reset' : 'Long Rest'}
        trigger_passive.__init__(self, origin, "features", desc, trigger, limit)

class Savage_Attacks(feature, trigger_passive):
    def __init__(self, origin):
        desc = "When you score a critical hit with a melee weapon " \
                    "attack, you can roll one of the weapon’s damage dice one " \
                    "additional time and add it to the extra damage of the " \
                    "critical hit. "
        trigger = ["Critical Hit"]
        limit = False
        trigger_passive.__init__(self, origin, "features", desc, trigger, limit)


class Divine_Sense(feature, action):
    def __init__(self, origin):
        desc = "The presence of strong evil registers on your senses like a " \
               "noxious odor, and powerful good rings like heavenly music in " \
               "your ears. As an action, you can open your awareness to " \
               "detect such forces. Until the end of your next turn, you know " \
               "the location of any celestial, fiend, or undead within 60 " \
               "feet of you that is not behind total cover. You know the type " \
               "(celestial, fiend, or undead) of any being whose presence you " \
               "sense, but not its identity (the vampire Count Strahd von " \
               "Zarovich, for instance). Within the same radius, you also " \
               "detect the presence of any place or object that has been " \
               "consecrated or desecrated, as with the Hallow spell. You can " \
               "use this feature a number of times equal to 1 + your Charisma " \
               "modifier. When you finish a long rest, you regain all " \
               "expended uses. "
        mod = char.attributes.CHA
        limit = {'num' : 1+mod,
                 'reset' : 'Long Rest'}
