import inspect
import sys

from actions import shove


class feat:

    def initial_effects(self, char):
        pass


def get_feats():
    feats = {}

    for feat in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if sys.modules[__name__].feat in feat[1].__bases__:
            feats[feat[0].replace("_", " ")] = feat[1]

    return feats


def get_feat(feat_name, origin):
    feat_list = get_feats()
    feat = feat_list[feat_name](origin)

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


class effect:

    def __init__(self, desc):
        self.desc = desc


class Actor(feat):

    def __init__(self, origin):
        self.desc = {"Skilled at mimicry and dramatics, you gain the "
                     "following benefits:":
                         ["+1 to Charisma",
                          "Advantage on Deception and Performance checks when "
                          "pretending to be someone else.",
                          "You can mimic the speech of another person or the "
                          "sounds made by other creatures. You must have "
                          "heard the person speaking, or heard the creature "
                          "make the sound, for at least 1 minute. A "
                          "successful Wisdom (Insight) check contested by "
                          "your Charisma (Deception) check allows a listener "
                          "to determine that the effect is faked."
                          ]}
        self.origin = origin
        super().__init__()

    def initial_effects(self, char):
        name = f'Feat: {self.__class__.__name__.replace("_", " ")}'

        char.attributes.CHA[name] = 1
        char.skills.deception['notes'][name] += [
            'Advantage when pretending to be '
            'someone else.']
        char.skills.performance['notes'][name] += [
            'Advantage when pretending to be '
            'someone else.']
        char.features[name] = ["You can mimic the speech of another "
                               "person or the sounds made by other "
                               "creatures. You must have heard the "
                               "person speaking, or heard the "
                               "creature make the sound, for at "
                               "least 1 minute. A successful Wisdom "
                               "(Insight) check contested by your "
                               "Charisma (Deception) check allows a "
                               "listener to determine that the "
                               "effect is faked."]

    @staticmethod
    def prereq():
        return False


class Heavily_Armored(feat):
    def __init__(self, origin):
        self.desc = {"You have trained to master the use of heavy armor, "
                     "gaining the following benefits:":
                         ['+1 to Strength',
                          'Heavy Armour proficiency']}

        self.origin = origin
        super().__init__()

    def initial_effects(self, char):
        name = f'Feat: {self.__class__.__name__.replace("_", " ")}'

        char.attributes.STR[name] = 1
        char.proficiencies.armor[name] = ['Heavy']

    @staticmethod
    def prereq():
        return ['armor', 'Medium']


class Shield_Master(feat):
    def __init__(self, origin):
        self.desc = {"You use shields not just for protection but also for "
                     "offense. You gain the following benefits while you are "
                     "wielding a shield:":
                         ["If you take the Attack action on your turn, "
                          "you can use a bonus action to try to shove a "
                          "creature within 5 feet of you with your shield.",
                          "If you aren’t incapacitated, you can add your "
                          "shield’s AC bonus to any Dexterity saving throw "
                          "you make against a spell or other harmful effect "
                          "that targets only you.",
                          "If you are subjected to an effect that allows you "
                          "to make a Dexterity saving throw to take only half "
                          "damage, you can use your reaction to take no "
                          "damage if you succeed on the saving throw, "
                          "interposing your shield between yourself and the "
                          "source of the effect."]}

        self.origin = origin
        super().__init__()

    def conditionals(self, char):

        name = f'Feat: {self.__class__.__name__.replace("_", " ")}'

        if 'Shield' in char.wielded.keys():

            char.saving_throws.DEX['notes'][name] = \
                ["If you aren’t incapacitated, you can add your shield’s AC "
                 "bonus to any Dexterity saving throw you make against a "
                 "spell or other harmful effect that targets only you.",
                 "If you are subjected to an effect that allows you to make a "
                 "Dexterity saving throw to take only half damage, you can "
                 "use your reaction to take no damage if you succeed on the "
                 "saving throw, interposing your shield between yourself and "
                 "the source of the effect."]

            char.actions.bonus['Shield Shove'] = {
                'desc': "If you take the Attack action on your turn, you can "
                        "use a bonus action to try to shove a creature within "
                        "5 feet of you with your shield.",
                'action': shove}
        else:
            try:
                del char.actions.bonus['Shield Shove']
                del char.saving_throws.DEX['notes'][name]
            except:
                pass

    @staticmethod
    def prereq():
        return False
