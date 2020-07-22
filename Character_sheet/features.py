import inspect
import sys

from actions import limited_action


def get_features():
    features = {}
    for feature_name, feature_object in inspect.getmembers(
            sys.modules[__name__], inspect.isclass):
        if sys.modules[
            __name__].feature in feature_object.__mro__ and not feature_object.__subclasses__():
            features[feature_name.replace("_", " ")] = feature_object

    return features


def get_feature(feature_name):
    features = get_features()

    return features[feature_name]()


class feature:
    def initial_effects(self, char):
        pass


class Darkvision(feature):
    def __init__(self):
        super().__init__()
        self.desc = 'You can see in dim light within 60 feet of you as if it ' \
                    'were bright light, and in darkness as if it were dim ' \
                    'light. You can’t discern color in darkness, only shades ' \
                    'of gray.'

    def initial_effects(self, char):
        char.features['Darkvision'] = self.desc


class Relentless_Endurance(feature):
    def __init__(self):
        super().__init__()
        self.desc = 'When you are reduced to 0 Hit Points but not killed ' \
                    'outright, you can drop to 1 hit point instead. You can’t ' \
                    'use this feature again until you finish a Long Rest. '
        # trigger = ["Zero HP"]
        # limit = {'num' : 1,
        #          'reset' : 'Long Rest'}


class Savage_Attacks(feature):
    def __init__(self):
        super().__init__()
        self.desc = "When you score a critical hit with a melee weapon " \
                    "attack, you can roll one of the weapon’s damage dice one " \
                    "additional time and add it to the extra damage of the " \
                    "critical hit. "
        # trigger = ["Critical Hit"]
        # limit = False

    def initial_effects(self, char):
        pass


class Divine_Sense(feature):
    def __init__(self):
        self.desc = "The presence of strong evil registers on your senses like a " \
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

    def initial_effects(self, char):
        limit = 1 + char.attributes.CHA.mod
        reset = 'Long Rest'
        char.actions.actions["Divine Sense"] = limited_action(self.desc, limit,
                                                              reset)

    def update(self, char):
        char.actions.actions[
            "Divine Sense"].max_uses = 1 + char.attributes.CHA.mod


class Lay_On_Hands(feature):
    def __init__(self):
        super().__init__()
        self.desc = f"You have a pool of healing power that can restore 5 X Paladin level HP per long rest. As an action, you can touch a creature to restore any number of HP remaining in the pool, or 5 HP to either cure a disease or neutralize a poison affecting the creature."
        # limit = {'num' : [5*char.classes[origin].level],
        #          'reset' : 'Long Rest'}
        # action_type = 'Free'
        # action.__init__(self, origin, "features", desc, action_type, limit)

        # def use(self, num):
        #     if self.current_uses + num <= self.max_uses:
        #         self.current_uses += num
        #     else:
        #         print("Not enough uses remaining!")
        #
        # char.actions.actions["Divine Sense"].use = MethodType(use, char.actions.actions["Divine Sense"])

    def initial_effects(self, char):
        pass
