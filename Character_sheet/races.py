import inspect
import sys

import helper_functions as f
from glossary import attrs, skills_dict


class race:

    def add_race_modifiers(self, char):

        race_key = {
            'race_name': ['info'],
            'size': ['stats', 'size'],
            'speed': ['stats', 'speed'],
            'languages': ['profficiencies', 'languages'],
            'attributes': ['attributes'],
            'skills': ['skills'],
            'feats': ['feats'],
            'features': ['features']}

        for trait in vars(self).keys():

            if trait in ['race_name', 'size', 'speed', 'languages']:
                path = f.LDK(char, race_key[trait])
                path['race'] = (getattr(self, trait))

            elif trait == 'attributes':
                for attr in self.attributes:
                    char.attributes[attr[0]]['race'] = attr[1]

            elif trait == 'skills':
                for skill in self.skills:
                    char.skills[skill].prof = True

            elif trait == 'feats':
                from feats import get_feat
                for feat in self.feats:
                    char.feats.race = get_feat(feat)
                    new_feat = char.feats.race
                    new_feat.add_feat_modifiers(char)

            elif trait == 'features':
                from features import get_feature
                for feature in self.features:
                    char.features['race'][feature] = get_feature(feature)()

    def remove_race_modifiers(self):
        pass


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
        self.languages = f.add_language(char.profficiencies.languages, 'Common', 1)


class Human(Human_Base):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = [(attr, 1) for attr in attrs]


class Human_Variant(Human_Base):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = f.add_attributes(attrs, 2)
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
        self.feats = f.add_feat(char, 1)
