from addict import Dict

from helper_functions import mod_calc
from glossary import skills_dict, attrs
from races import get_race
from classes import get_class

class character:

    def __init__(self):
        self.sheet = Dict()

    def create_character(self):
        sheet = Dict()

        sheet.info = Dict({'alignment': None,
                          'level': None,
                          'fore_name': None,
                          'middle_name': None,
                          'family_name': None,
                          'race': None
                           })

        sheet.bio = Dict({'faith': None
                          })

        sheet.stats = Dict({'max_hp': None,
                           'current_hp': None,
                           'armour_class': None,
                           'defences': None,
                           'conditions': None,
                           'size': Dict({'race': None, 'temp': None}),
                           'speed': Dict({'race': None, 'mod': None})
                            })

        sheet.attributes = Dict({attr: Dict({'base': None,
                                            'override': None})
                                 for attr in attrs})

        sheet.skills = Dict({skill: Dict({'name': skills_dict[skill][0],
                                         'attr': skills_dict[skill][1],
                                         'prof': False})
                             for skill in skills_dict})

        sheet.saving_throws = Dict({attr: Dict({'mod': None,
                                               'override': None,
                                               'prof': False})
                                    for attr in attrs})

        sheet.profficiencies = Dict({'languages': Dict(),
                                    'armor': Dict(),
                                    'weapons': Dict({"Base": ["Unarmed"]}),
                                    'tools': Dict(),
                                    'other': Dict()
                                     })

        sheet.actions = Dict({'actions': Dict(),
                             'bonus': Dict(),
                             'attack': Dict(),
                             'reaction': Dict()})

        sheet.feats = Dict()

        sheet.features = Dict()

        self.sheet = sheet


    def choose_class(self, class_choice):
        starting_class = get_class(char, class_choice)
        starting_class.add_class_features(self.sheet)

    def choose_race(self, race_name):
        race = get_race(self.sheet, race_name)  # TODO: Make this input at
        # some point
        race.add_race_modifiers(self.sheet)

    def update(self):
        ### Modifiers
        attrs = self.sheet.attributes
        for attr_name, attr in attrs.items():

            if attr.override:
                attrs[attr_name].mod = mod_calc(attr.override)
                break
            else:
                total = sum([attr[val] for val in attr if type(attr[val]) ==
                           int])
                if total < 0:
                    total = 0
                attrs[attr_name].stat = total
                attrs[attr_name].mod = mod_calc(total)


        ### HP calculation

        classes = self.sheet.classes



char = character()
char.create_character()
char.choose_class("Test") # automatically run these on creating a character
char.choose_race("Half Orc")
char.update()


print("Done!")
