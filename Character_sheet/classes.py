import inspect
import sys

from addict import Dict

import helper_functions as f


class Class:

    def add_class_features(self, char):
        ## If first class do stuff like HP, saves
        ## Multiclass profficiencies are listed in table
        if not char.classes:
            for trait in vars(self).keys():

                if trait == 'saves':
                    for save in self.saves:
                        char.saving_throws[save].prof = True

                elif trait == 'prof_weapons':
                    char.profficiencies.weapons[self.class_name + '_origin'] = self.prof_weapons
                elif trait == 'prof_armor':
                    char.profficiencies.armor[self.class_name + '_origin'] = self.prof_armor
                elif trait == 'prof_tools':
                    char.profficiencies.tools[self.class_name + '_origin'] = self.prof_tools

                elif trait == 'equipment':
                    self.equipment = f.choose_weapons(self.equipment)  ## Choose weapons only when adding
                    for item in self.equipment:
                        from items import get_item
                        if item[0] in char.equipment:
                            char.equipment[item[0]].add_number(item[1])
                        else:
                            char.equipment.update({item[0]: get_item(item[0], item[1])})

        char.classes.update(Dict({self.class_name: {'level': 1,
                                                    'hit_dice': 10,
                                                    'lvl_up_hp': 6}}))


def get_class(char, choice):
    classes = {}

    for class_name in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if not class_name[1].__subclasses__():
            classes[class_name[0].replace("_", " ")] = class_name[1]

    class_choice = classes[choice](char)

    return class_choice


class Paladin(Class):
    def __init__(self, char):
        self.class_name = 'Paladin'
        self.hit_dice = 10
        self.hit_points = 6
        self.prof_armor = ["Light", "Medium", "Heavy", "Shields"]
        self.prof_weapons = ["Simple", "Martial"]
        self.prof_tools = None
        self.saves = ["WIS", "CHA"]
        allowed_skills = ["athletics", "insight", "intimidation", "medicine", "persuasion", "religion"]
        self.skills = f.add_skill(char.skills, allowed_skills, 2)
        self.equipment = []

        choice = f.simple_choice(['One martial weapon and a shield', 'Two martial weapons'])
        inv = {0: [('Weapon', 1, 'Martial', 'Any'), ('Shield', 1)],
               1: [('Weapon', 1, 'Martial', 'Any'), ('Weapon', 1, 'Martial', 'Any')]}
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


class Test(Class):
    def __init__(self, char):
        self.class_name = 'Test'
        self.hit_dice = 0
        self.hit_points = 0
        self.prof_armor = ["Light", "Medium", "Heavy", "Shields"]
        self.prof_weapons = ["Simple", "Martial"]
        self.saves = ["WIS", "CHA"]
        self.equipment = [('Weapon', 1, 'Martial', 'Melee'), ('Weapon', 1, 'Simple', 'Melee')]

        print(self.equipment)