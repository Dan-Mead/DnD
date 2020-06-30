import helper_functions as f
from glossary import *

class Class:
    pass


def get_class(char, choice):

    class_list = {"Paladin" : Paladin,
                    }

    class_choice = class_list[choice](char)

    return class_choice

class Paladin(Class):
    def __init__(self, char):
        self.hit_dice = 10
        self.hit_points = 6
        self.prof_armor = ["Light", "Medium", "Heavy", "Shields"]
        self.prof_weapons = ["Simple", "Martial"]
        self.saves = ["WIS", "CHA"]
        allowed_skills = ["athletics", "insight", "intimidation", "medicine", "persuasion", "religion"]
        # self.skills = f.add_skill(char.skills, allowed_skills, 2)
        self.equipment = []

        choice = f.simple_choice(['One martial weapon and a shield', 'Two martial weapons'])
        inv = {0 : [('Martial Weapon', 1), ('Shield', 1)],
                1 : [('Martial Weapon', 1), ('Martial Weapon', 1)]} ### TODO: Add as actual objects
        self.equipment += inv[choice]

        choice = f.simple_choice(['Five javelins', 'One simple melee weapon'])
        inv = {0 : [('Javelin', 5)],
                1 : [('Simple Weapon', 1)]}
        self.equipment += inv[choice]

        choice = f.simple_choice(["Priest's pack", "Explorer's pack"])
        inv = {0 : [('Priest Pack', 1)],
                1 : [('Explorer Pack', 1)]} ### TODO: Add as actual objects
        self.equipment += inv[choice]
        self.equipment += [('Chain Mail', 1), ('Holy Symbol', 1)]

        ### Add backgrounf shit here