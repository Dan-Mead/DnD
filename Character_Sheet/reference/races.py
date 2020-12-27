from .features import *
from .glossary import all_languages
from .skills_and_attributes import *


class Race:
    pass


class Human(Race):
    race_name = "Human"
    speed = 30
    size = "Medium"
    languages = ("Common", all_languages)
    features = None

    @staticmethod
    def prereq():
        return False


class HumanBase(Human):
    subrace_name = "Base"
    ASI = tuple(zip(attr_list.values(), [1] * len(attr_list)))
    features = None


class HumanVariant(Human):
    subrace_name = "Variant"
    ASI = ((list(attr_list.values()), 2),)
    features = ["skills", "feat"]
    skills = ("any",)
    feats = "any"


class HalfOrc(Race):
    race_name = "Half-Orc"
    speed = 30
    size = "Medium"
    languages = ("Common", "Orc")
    ASI = ((STR, +2), (CON, +1))
    features = ["other"]
    other_features = {'Darkvision': Darkvision("Orc", 60),
                      'Menacing': Menacing(),
                      'Relentless Endurance': RelentlessEndurance(),
                      'Savage Attacks': SavageAttacks()
                      }


class HalfElf(Race):
    race_name = "Half-Elf"
    speed = 30
    size = "Medium"
    languages = ("Common", "Elvish", all_languages)
    ASI = ((CHA, +2), ([a for a in (attr_list.values()) if a is not CHA], 2))
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
    skills = ("any", "any")


class MoonElfDescent(HalfElf):
    subrace_name = "Moon Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = ("any", "any")


class SunElfDescent(HalfElf):
    subrace_name = "Sun Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = ("any", "any")


class DrowDescent(HalfElf):
    subrace_name = "Drow Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Drow Magic": DrowMagic()}
    skills = ("any", "any")


class AquaticElfDescent(HalfElf):
    subrace_name = "Aquatic Elf Descent"
    features = ["choice"]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Swim": Swim()}
    skills = ("any", "any")


race_list = dict([(race.race_name, race) for race in Race.__subclasses__()])

if __name__ == '__main__':
    pass
