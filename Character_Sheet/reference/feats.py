import inspect
import sys

class Feat:
    pass

class Actor(Feat):
    name = "Actor"
    prereq = False
    desc = {"Skilled at mimicry and dramatics, you gain the "
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


class Heavily_Armored(Feat):
    name = "Heavily Armored"
    prereq = ['armor', 'medium']
    desc = {"You have trained to master the use of heavy armor, "
                     "gaining the following benefits:":
                         ['+1 to Strength',
                          'Heavy Armour proficiency']}


class Shield_Master(Feat):
    name = "Shield Master"
    prereq = False
    desc = {"You use shields not just for protection but also for "
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

feat_list = dict([(feat.name, feat) for feat in Feat.__subclasses__()])

def unpack_desc(entry):
    text = list(entry.keys())
    text += [point for item in entry.values() for point in item]
    text = "\n\n * ".join(text)
    return text
