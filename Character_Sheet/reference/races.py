from Character_Sheet.reference.features import *
from Character_Sheet.reference.glossary import all_languages
from Character_Sheet.reference.skills_and_attributes import *
from Character_Sheet.reference.feats import feat_list
import Character_Sheet.reference.items.tools as tools

import Character_Sheet.helpers as helpers


class Race:
    pass


class FeatureType:
    choice = "choice_features"
    other = "other_features"
    skills = "skills"
    feats = "feats"
    tools = "tool"
    proficiencies = "proficiencies"


class RaceFeatures:
    def __init__(self, features_dict):
        self.types = set()
        self.all = features_dict
        self.choices = []

        for feature_name in features_dict:
            feature_values = features_dict[feature_name]
            if isinstance(feature_values, list):
                for pair in feature_values:
                    self.types.add(pair[0])
                    if pair[0] == FeatureType.choice:
                        self.choices.append(feature_name)
            else:
                self.types.add(feature_values[0])
                if feature_values[0] == FeatureType.choice:
                    self.choices.append(feature_name)


class Human(Race):
    race_name = "Human"
    speed = 30
    size = "Medium"
    languages = ("Common", all_languages)
    features = None


class HumanBase(Human):
    subrace_name = "Base"
    ASI = tuple(zip(attr_list.values(), [1] * len(attr_list)))
    features = None


class HumanVariant(Human):
    subrace_name = "Variant"
    ASI = ((list(attr_list.values()), 2),)
    skills = (list(skills_list.keys()),)
    feats = (list(feat_list.keys()),)
    features = RaceFeatures({"Human Ambition": [(FeatureType.skills, skills),
                                                (FeatureType.feats, feats)]
                             })


class HalfOrc(Race):
    race_name = "Half-Orc"
    speed = 30
    size = "Medium"
    languages = ("Common", "Orc")
    ASI = ((STR, +2), (CON, +1))
    features = RaceFeatures({'Darkvision': (FeatureType.other, Darkvision("Orc", 60)),
                             'Menacing': (FeatureType.other, Menacing()),
                             'Relentless Endurance': (FeatureType.other, RelentlessEndurance()),
                             'Savage Attacks': (FeatureType.other, SavageAttacks())
                             })


class HalfElf(Race):
    race_name = "Half-Elf"
    speed = 30
    size = "Medium"
    languages = ("Common", "Elvish", all_languages)
    ASI = ((CHA, +2), ([a for a in (attr_list.values()) if a is not CHA], 2))
    features = RaceFeatures({'Darkvision': (FeatureType.other, Darkvision("Elf", 60)),
                             'Fey Ancestry': (FeatureType.other, FeyAncestry())
                             })


class WoodElfDescent(HalfElf):
    subrace_name = "Wood Elf Descent"
    skills = (list(skills_list.keys()), list(skills_list.keys()))
    choice_features = {"Skill Versatility": (FeatureType.skills, skills),
                       "Keen Senses": (FeatureType.other, KeenSenses()),
                       "Elf Weapon Training": (FeatureType.other, ElfWeaponTraining()),
                       "Fleet of Foot": (FeatureType.other, FleetOfFoot()),
                       "Mask of the Wild": (FeatureType.other, MaskOfTheWild())
                       }
    features = RaceFeatures({'Half-Elf Versatility': (FeatureType.choice, choice_features)})


class MoonElfDescent(HalfElf):
    subrace_name = "Moon Elf Descent"
    skills = (list(skills_list.keys()), list(skills_list.keys()))
    choice_features = {"Skill Versatility": (FeatureType.skills, skills),
                       "Keen Senses": (FeatureType.other, KeenSenses()),
                       "Elf Weapon Training": (FeatureType.other, ElfWeaponTraining()),
                       "Cantrip": (FeatureType.other, Catrip("one", "Wizard", "Intelligence"))
                       }
    features = RaceFeatures({'Half-Elf Versatility': (FeatureType.choice, choice_features)})


class SunElfDescent(HalfElf):
    subrace_name = "Sun Elf Descent"
    skills = (list(skills_list.keys()), list(skills_list.keys()))
    choice_features = {"Skill Versatility": (FeatureType.skills, skills),
                       "Keen Senses": (FeatureType.other, KeenSenses()),
                       "Elf Weapon Training": (FeatureType.other, ElfWeaponTraining()),
                       "Cantrip": (FeatureType.other, Catrip("one", "Wizard", "Intelligence"))
                       }
    features = RaceFeatures({'Half-Elf Versatility': (FeatureType.choice, choice_features)})


class DrowDescent(HalfElf):
    subrace_name = "Drow Descent"
    skills = (list(skills_list.keys()), list(skills_list.keys()))
    choice_features = {"Skill Versatility": (FeatureType.skills, skills),
                       "Keen Senses": (FeatureType.other, KeenSenses()),
                       "Drow Magic": (FeatureType.other, DrowMagic())}
    features = RaceFeatures({'Half-Elf Versatility': (FeatureType.choice, choice_features)})


class AquaticElfDescent(HalfElf):
    subrace_name = "Aquatic Elf Descent"
    skills = (list(skills_list.keys()), list(skills_list.keys()))
    choice_features = {"Skill Versatility": (FeatureType.skills, skills),
                       "Keen Senses": (FeatureType.other, KeenSenses()),
                       "Swim": (FeatureType.other, Swim())}
    features = RaceFeatures({'Half-Elf Versatility': (FeatureType.choice, choice_features)})


class Loxodon(Race):
    race_name = "Loxodon"
    speed = 30
    size = "Medium"
    ASI = ((CON, 2), (WIS, 1))
    languages = ("Common", "Loxodon")
    features = RaceFeatures({"Powerful Build": (FeatureType.other, PowerfulBuild()),
                             "Loxodon Serenity": (FeatureType.other, LoxodonSerenity()),
                             "Natural Armour": (FeatureType.other, NaturalArmour()),
                             "Trunk": (FeatureType.other, Trunk()),
                             "Keen Smell": (FeatureType.other, KeenSmell())
                             })


class Warforged(Race):
    race_name = "Warforged"
    speed = 30
    size = "Medium"
    ASI = ((CON, 2), ([a for a in (attr_list.values()) if a is not CON], 1))
    skills = (list(skills_list.keys()),)
    languages = ("Common", all_languages)
    features = RaceFeatures({"Constructed Resilience": (FeatureType.other, ConstructedResilience()),
                             "Sentry's Rest": (FeatureType.other, SentrysRest()),
                             "Integrated Protection": (FeatureType.other, IntegratedProtection()),
                             "Specialised Design": [(FeatureType.skills, skills),
                                                    (FeatureType.proficiencies, (FeatureType.tools, (
                                                    [tool.name for tool in
                                                     helpers.list_end_values(tools.Tool)],)))]
                             })


class Dwarf(Race):
    race_name = "Dwarf"
    speed = 25
    size = "Medium"
    ASI = ((CON, 2),)
    languages = ("Common", "Dwarvish")

    features = RaceFeatures({"Darkvision": (FeatureType.other, Darkvision2("Accustomed to life underground", 60)),
                             "Dwarven Resilience": (FeatureType.other, DwarvenResilience()),
                             "Dwarven Stoutness": (FeatureType.other, DwarvenStoutness()),
                             "Dwarven Combat Training": (FeatureType.other, DwarvenCombatTraining()),
                             "Tool Proficiency": (FeatureType.proficiencies, (FeatureType.tools, ([tools.Smith.name,
                                                                                                   tools.Brewer.name,
                                                                                                   tools.Mason.name],))),
                             "Stonecunning": (FeatureType.other, Stonecunning())})


class HillDwarf(Dwarf):
    subrace_name = "Hill Dwarf"
    ASI = ((WIS, 1),)
    features = RaceFeatures({"Dwarven Toughness": (FeatureType.other, DwarvenToughness())})


class MountainDwarf(Dwarf):
    subrace_name = "Mountain Dwarf"
    ASI = ((STR, 2),)
    features = RaceFeatures({"Dwarven Armour Training": (FeatureType.other, DwarvenArmourTraining())})


class Duergar(Dwarf):
    subrace_name = "Duergar (Grey Dwarf)"
    ASI = ((STR, 1),)
    features = RaceFeatures({"Superior Darkvision": (FeatureType.other, SuperiorDarvision(120)),
                             "Duergar Resilience": (FeatureType.other, DuergarResilience()),
                             "Duergar Magic": (FeatureType.other, DuergarMagic()),
                             "Sunlight Sensitivity": (FeatureType.other, SunlightSensitivity())})


if __name__ == '__main__':
    pass
else:
    race_list = dict([(race.race_name, race) for race in Race.__subclasses__()])
