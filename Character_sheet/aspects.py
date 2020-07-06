from addict import Dict

from glossary import skills_dict, attrs
from races import get_race
from classes import get_class


def create_character():

    def __init__(self):

        self.info = Dict({'alignment': None,
                          'level': None,
                          'fore_name': None,
                          'middle_name': None,
                          'family_name': None,
                          'race': None
                          })

        self.bio = Dict({'faith': None
                         })

        self.stats = Dict({'max_hp': None,
                           'current_hp': None,
                           'armour_class': None,
                           'defences': None,
                           'conditions': None,
                           'size': Dict({'race': None, 'temp': None}),
                           'speed': Dict({'race': None, 'mod': None})
                           })

        self.attributes = Dict({attr: Dict({'base': None,
                                            'override': None})
                                for attr in attrs})

        self.skills = Dict({skill: Dict({'name': skills_dict[skill][0],
                                         'attr': skills_dict[skill][1],
                                         'prof': False})
                            for skill in skills_dict})

        self.saving_throws = Dict({attr: Dict({'mod': None,
                                               'override': None,
                                               'prof': False})
                                   for attr in attrs})

        self.profficiencies = Dict({'languages': Dict(),
                                    'armor': Dict(),
                                    'weapons': Dict({"Base": ["Unarmed"]}),
                                    'tools': Dict(),
                                    'other': Dict()
                                    })

        self.actions = Dict({'actions': Dict(),
                             'bonus': Dict(),
                             'attack': Dict(),
                             'reaction': Dict()})

        self.feats = Dict()

        self.features = Dict()


def choose_class(character, class_choice):
    starting_class = get_class(char, class_choice)
    starting_class.add_class_features(character)
    char.classes[class_choice]

def choose_race(character, race_name):
    race = get_race(character, race_name)  # TODO: Make this input at some point
    race.add_race_modifiers(character)


char = create_character()

choose_class(char, "Test")

choose_race(char, "Half Orc")

class_ = char.classes.Test

class_.level_up("Test")

print("Done!")
