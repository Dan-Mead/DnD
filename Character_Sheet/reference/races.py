from .features import *
from .glossary import all_languages
from .skills_and_attributes import *
from .feats import feat_list


class Race:
    pass

class FeatureType:
    choice = "choice"
    other = "other"
    skills = "skills"
    feats = "feats"


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
    features = [FeatureType.skills, FeatureType.feats]
    skills = (list(skills_list.keys()),)
    feats = (list(feat_list.keys()),)


class HalfOrc(Race):
    race_name = "Half-Orc"
    speed = 30
    size = "Medium"
    languages = ("Common", "Orc")
    ASI = ((STR, +2), (CON, +1))
    features = [FeatureType.other]
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
    features = [FeatureType.other]
    other_features = {'Darkvision': Darkvision("Elf", 60),
                      'Fey Ancestry': FeyAncestry()
                      }


class WoodElfDescent(HalfElf):
    subrace_name = "Wood Elf Descent"
    features = [FeatureType.choice]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Fleet of Foot": FleetOfFoot(),
                       "Mask of the Wild": MaskOfTheWild()}
    skills = (list(skills_list.keys()), list(skills_list.keys()))


class MoonElfDescent(HalfElf):
    subrace_name = "Moon Elf Descent"
    features = [FeatureType.choice]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = (list(skills_list.keys()), list(skills_list.keys()))


class SunElfDescent(HalfElf):
    subrace_name = "Sun Elf Descent"
    features = [FeatureType.choice]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Elf Weapon Training": ElfWeaponTraining(),
                       "Cantrip": Catrip("one", "Wizard", "Intelligence")}
    skills = (list(skills_list.keys()), list(skills_list.keys()))


class DrowDescent(HalfElf):
    subrace_name = "Drow Descent"
    features = [FeatureType.choice]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Drow Magic": DrowMagic()}
    skills = (list(skills_list.keys()), list(skills_list.keys()))


class AquaticElfDescent(HalfElf):
    subrace_name = "Aquatic Elf Descent"
    features = [FeatureType.choice]
    choice_features = {"Skill Versatility": "skills",
                       "Keen Senses": KeenSenses(),
                       "Swim": Swim()}
    skills = (list(skills_list.keys()), list(skills_list.keys()))


race_list = dict([(race.race_name, race) for race in Race.__subclasses__()])

if __name__ == '__main__':
    pass
