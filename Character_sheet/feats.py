import inspect
import sys

from effects import modifier, note, passive_effect, action


class feat:
    def __init__(self):
        self.origin = " : ".join(['feat', self.__class__.__name__.replace("_", " ")])

    def add_feat_modifiers(self, char):
        for effect in self.effects:
            effect.add_effect(char)


def get_feats():
    feats = {}

    for feat in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if sys.modules[__name__].feat in feat[1].__bases__:
            feats[feat[0].replace("_", " ")] = feat[1]

    return feats


def get_feat(feat_name):
    feat_list = get_feats()
    feat = feat_list[feat_name]()

    return feat


def get_valid_feats(char):
    feats_list = get_feats()

    valid_feats = []

    for feat in feats_list:
        prereq = feats_list[feat].prereq()
        if not prereq:
            valid_feats.append(feat)
        elif prereq[0] == 'armor':
            groups = char.proficiencies.armor.values()
            armors = [armor for group in groups for armor in group]
            if prereq[1] in armors:
                valid_feats.append(feat)

    return valid_feats


class Actor(feat):
    def __init__(self):
        super().__init__()

        self.desc = "Skilled at mimicry and dramatics, you gain the following " \
                    "benefits: "
        self.effects = [modifier(self.origin, "attributes.CHA", +1),
                        note(self.origin, "skills.deception.notes",
                             "Advantage when pretending to be someone else."),
                        note(self.origin, "skills.performance.notes",
                             "Advantage when pretending to be someone else."),
                        passive_effect(self.origin, "features",
                                       "You can mimic the speech of another "
                                       "person or the sounds made by other "
                                       "creatures. You must have heard the "
                                       "person speaking, or heard the creature "
                                       "make the sound, for at least 1 minute. "
                                       "A successful Wisdom (Insight) check "
                                       "contested by your Charisma (Deception) "
                                       "check allows a listener to determine "
                                       "that the effect is faked.")
                        ]

    @staticmethod
    def prereq():
        return False


class Heavily_Armored(feat):
    def __init__(self):
        super().__init__()
        self.desc = "You have trained to master the use of heavy armor, gaining " \
                    "the following benefits: "
        self.effects = [modifier(self.origin,
                                 "attributes.STR",
                                 +1),
                        modifier(self.origin,
                                 "proficiencies.armor",
                                 "Heavy")]

    @staticmethod
    def prereq():
        return ['armor', 'Medium']


class Shield_Master(feat):
    def __init__(self):
        super().__init__()
        self.desc = "You use shields not just for protection but also for " \
                    "offense. You gain the following benefits while you are " \
                    "wielding a shield:",
        self.effects = [action(self.origin,
                               "actions.bonus",
                               "If you take the Attack action on your turn, "
                               "you can use a bonus action to try to shove a "
                               "creature within 5 feet of you with your shield."),
                        note(self.origin,
                             "saving_throws.DEX.notes",
                             "Add shield's AC bonus if only you are targeted "
                             "by spell or harmful effect, and if not "
                             "incapacitated."),
                        note(self.origin,
                             "saving_throws.DEX.notes",
                             "You can use your reaction to take no damage, "
                             "if successful on a saving throw to take half "
                             "damage from an effect.")]

    @staticmethod
    def prereq():
        return False
