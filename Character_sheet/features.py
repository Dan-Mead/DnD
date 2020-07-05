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
        limit = [1, "Long Rest"]
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