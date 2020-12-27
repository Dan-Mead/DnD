import inspect
import sys

import helper_functions as f
from features import get_feature
from items import get_item


class character_class:
    def __init__(self, level, hit_dice, lvl_up_hp, first):
        self.level = level
        self.hit_dice = hit_dice
        self.lvl_up_hp = lvl_up_hp
        self.base_class = first

    def level_up(self):
        self.level += 1

        # level_table = getattr(sys.modules[__name__], class_name).levels()

        ### Add new level features


class Class:

    def add_class_features(self, char):

        if not hasattr(char, 'classes'):

            char.classes = Dict()

            origin = 'origin: ' + self.class_name

            for trait in vars(self).keys():

                if trait == 'saves':
                    for save in self.saves:
                        char.saving_throws[save].prof += [origin]

                elif trait == 'skills':
                    for skill in self.skills:
                        char.skills[skill].prof += [origin]

                elif trait == 'prof_weapons':
                    char.proficiencies.weapons[origin] = self.prof_weapons
                elif trait == 'prof_armor':
                    char.proficiencies.armor[origin] = self.prof_armor
                elif trait == 'prof_tools':
                    char.proficiencies.tools[origin] = self.prof_tools

                elif trait == 'equipment':
                    self.equipment = f.choose_weapons(self.equipment)
                    for item in self.equipment:
                        if item[0] in char.equipment:
                            char.equipment[item[0]].add_number(item[1])
                        else:
                            char.equipment.update(
                                {item[0]: get_item(item[0], item[1])})

                elif trait not in ['class_name', 'hit_dice', 'hit_points',
                                   'levels']:
                    raise Exception(
                        f"{trait} included which haven't been added.")

            char.classes[self.class_name] = character_class(1, self.hit_dice,
                                                            self.hit_points,
                                                            True)
        else:
            char.classes[self.class_name] = character_class(1, self.hit_dice,
                                                            self.hit_points,
                                                            False)

        for feature in self.levels[1]:
            new_feature = get_feature(feature)
            char.features[f"Class: {self.class_name}"][feature] = new_feature
            new_feature.initial_effects(char)


def get_class(char, choice):
    classes = {}

    for class_name in inspect.getmembers(sys.modules[__name__],
                                         inspect.isclass):
        if not class_name[1].__subclasses__():
            classes[class_name[0].replace("_", " ")] = class_name[1]

    class_choice = classes[choice](char)

    return class_choice


class Paladin(Class):
    def __init__(self, char):
        self.class_name = 'Paladin'
        self.hit_dice = 10
        self.hit_points = 6
        self.prof_armor = ["Light", "Medium", "Heavy", "Shield"]
        self.prof_weapons = ["Simple", "Martial"]
        self.saves = ["WIS", "CHA"]
        allowed_skills = ["athletics", "insight", "intimidation", "medicine",
                          "persuasion", "religion"]
        self.skills = f.add_skill(char.skills, allowed_skills, 2)
        self.equipment = []

        choice = f.simple_choice(
            ['One martial weapon and a shield', 'Two martial weapons'])
        inv = {0: [('Weapon', 1, 'Martial', 'Any'), ('Shield', 1)],
               1: [('Weapon', 1, 'Martial', 'Any'),
                   ('Weapon', 1, 'Martial', 'Any')]}
        self.equipment += inv[choice]

        choice = f.simple_choice(['Five javelins', 'One simple melee weapon'])
        inv = {0: [('Javelin', 5)],
               1: [('Weapon', 1, 'Simple', 'Melee')]}
        self.equipment += inv[choice]

        choice = f.simple_choice(["Priest's pack", "Explorer's pack"])
        inv = {0: [('Priest Pack', 1)],
               1: [('Explorer Pack', 1)]}
        self.equipment += inv[choice]
        self.equipment += [('Chain Mail', 1), ('Holy Symbol', 1)]

        self.levels = {1: ['Divine Sense', 'Lay On Hands'],
                       2: ['Divine Smite', 'Fighting Style', 'Spellcasting']}

    @staticmethod
    def levels():
        levels = {1: ['Divine Sense', 'Lay On Hands'],
                  2: ['Divine Smite', 'Fighting Style', 'Spellcasting']}
        return levels


class Test(Class):
    def __init__(self, char):
        self.class_name = 'Paladin'
        self.hit_dice = 10
        self.hit_points = 6
        allowed_skills = ["athletics", "insight", "intimidation", "medicine",
                          "persuasion", "religion"]
        # self.skills = f.add_skill(char.skills, allowed_skills, 2)
        self.prof_armor = ["Light", "Medium", "Heavy", "Shield"]
        # self.prof_armor = ["Light", "Medium"]
        self.prof_weapons = ["Simple", "Martial"]
        # self.prof_weapons = ["Simple"]
        self.saves = ["WIS", "CHA"]
        self.equipment = [('Chain Mail', 1)]
        self.equipment += [('Holy Symbol', 1),
                           ('Shield', 1),
                           ('Warhammer', 1),
                           ('Shortsword', 1),
                           ('Glaive', 1),
                           ('Lance', 1),
                           ('Handaxe', 1)]

        self.levels = {1: ['Divine Sense', 'Lay On Hands'],
                       2: ['Divine Smite', 'Fighting Style', 'Spellcasting']}
