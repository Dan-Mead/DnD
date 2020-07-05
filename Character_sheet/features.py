import inspect
import sys

from effects import passive_effect, trigger_passive, active_effect

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
    def __init__(self):
        self.desc = 'You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if ' \
                    'it were dim light. You can’t discern color in Darkness, only Shades of Gray. '


class Relentless_Endurance(feature, trigger_passive):
    def __init__(self):
        self.desc = 'When you are reduced to 0 Hit Points but not killed outright, you can drop to 1 hit point ' \
                    'instead. You can’t use this feature again until you finish a Long Rest. '
        self.trigger = ["Zero HP"]
        self.limited = [1, "Long Rest"]


class Savage_Attacks(feature, trigger_passive):
    def __init__(self):
        self.desc = 'When you score a critical hit with a melee weapon Attack, you can roll one of the weapon’s ' \
                    'damage dice one additional time and add it to the extra damage of the critical hit. '
        self.trigger = ["Critical Hit"]
        self.limited = False
