import inspect
import sys

import helper_functions as f
from glossary import attrs, skills_dict


class race:

    def add_race_modifiers(self, char):

        char.info.Race = self.race_name
        char.stats.size.Race = self.size
        char.stats.speed.Race = self.speed
        char.proficiencies.languages.Race = self.languages

        for trait in vars(self).keys():
            if trait == 'attributes':
                for attr in self.attributes:
                    char.attributes[attr[0]]['race'] = attr[1]

            elif trait == 'skills':
                for skill in self.skills:
                    char.skills[skill].prof += [self.race_name]

            elif trait == 'feats':
                from feats import get_feat
                for feat in self.feats:
                    new_feat = get_feat(feat, self.race_name)
                    char.feats[feat] = new_feat
                    char.feats[feat].initial_effects(char)


            elif trait == 'features':
                from features import get_feature
                for feature in self.features:
                    new_feature = get_feature(feature)
                    char.features[self.race_name][feature] = new_feature
                    new_feature.initial_effects(char)

            elif trait not in ['race_name', 'size', 'speed', 'languages']:
                raise Exception(f"{trait} included which hasn't been added.")


def get_race(char, race_choice):
    races = {}

    for race in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if not race[1].__subclasses__():
            races[race[0].replace("_", " ")] = race[1]

    race = races[race_choice](char)

    return race


class Human_Base(race):
    def __init__(self, char):
        self.race_name = "Human"
        self.size = 'Medium'
        self.speed = 30
        self.languages = f.add_language(char.proficiencies.languages, 'Common',
                                        1)


class Human(Human_Base):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = [(attr, 1) for attr in attrs]


class Human_Variant(Human_Base):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = [(attr, 1) for attr in f.add_attributes(attrs, 2)]
        self.skills = f.add_skill(char.skills, skills_dict.keys(), 1)
        self.feats = f.add_feat(char, 1)


class Half_Orc(race):
    def __init__(self, char):
        self.race_name = "Half-Orc"
        self.size = "Medium"
        self.speed = 30
        self.attributes = [("STR", 2), ("CON", 1), ("INT", -2)]
        self.features = ["Darkvision", "Relentless Endurance", "Savage Attacks"]
        self.skills = ["intimidation"]
        self.languages = ["Common", "Orc"]


class Test(race):
    def __init__(self, char):
        self.race_name = "Test Race"
        self.size = "Medium"
        self.speed = 30
        self.languages = ["Common"]
        # self.languages = f.add_language(char.proficiencies.languages, 'Common', 1)
        # self.attributes = [(attr, 1) for attr in f.add_attributes(attrs, 2)]
        # self.feats = f.add_feat(char, 1)
        self.features = ["Darkvision", "Relentless Endurance", "Savage Attacks"]
