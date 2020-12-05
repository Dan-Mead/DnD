import inspect
import sys
from glossary import attrs
from features import *


class Race:
    pass


class Human(Race):
    name = "Human"
    speed = 30
    size = "Medium"
    languages = ("Common", "choice")
    features = None

    @staticmethod
    def prereq():
        return False


class HumanBase(Human):
    subrace_name = "Base"
    ASI = tuple(zip(attrs, [1] * len(attrs)))
    features = None


class HumanVariant(Human):
    subrace_name = "Variant"
    ASI = (("choice", "any"), ("choice", "any"))
    features = ["skills", "feat"]
    skills = "any"
    feats = "any"


class HalfOrc(Race):
    name = "Half-Orc"
    speed = 30
    size = "Medium"
    languages = ("Common", "Orc")
    ASI = (("STR", +2), ("CON", +1))
    features = ["other"]
    other_features = {'Darkvision': Darkvision("Orc", 60),
                      'Menacing': Menacing(),
                      'Relentless Endurance': RelentlessEndurance(),
                      'Savage Attacks': SavageAttacks()
                      }


class HalfElf(Race):
    name = "Half-Elf"
    speed = 30
    size = "Medium"
    languages = ("Common", "Elvish", "choice")
    ASI = (("CHA", +2), ("choice", "CHA"), ("choice", "CHA"))
    features = ["other"]
    other_features = {'Darkvision': Darkvision("Elf", 60),
                      'Fey Ancestry': FeyAncestry()
                      }


class WoodElfDescent(HalfElf):
    subrace_name = "Wood Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Fleet of Foot": FleetOfFoot(),
                       "Mask of the Wild": MaskOfTheWild()}
    skills = ["any", "any"]


class MoonElfDescent(HalfElf):
    subrace_name = "Moon Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = ["any", "any"]


class SunElfDescent(HalfElf):
    subrace_name = "Sun Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = ["any", "any"]


class DrowDescent(HalfElf):
    subrace_name = "Drow Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Drow Magic": DrowMagic()}
    skills = ["any", "any"]


class AquaticElfDescent(HalfElf):
    subrace_name = "Aquatic Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Swim": Swim()}
    skills = ["any", "any"]


race_list = dict([(race.name, race) for race in Race.__subclasses__()])

# race_list = dict(zip())

# for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
#
#
#
#     print(name, obj)
#     print(issubclass(obj, race))
