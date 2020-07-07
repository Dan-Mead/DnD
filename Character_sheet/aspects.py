from addict import Dict

from helper_functions import mod_calc
from glossary import skills_dict, attrs
from races import get_race
from classes import get_class


class character:

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

        self.attributes = Dict({attr: Dict({'base': 10,
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

        self.equipment = Dict()

    def choose_class(self, class_choice):
        starting_class = get_class(char, class_choice)
        starting_class.add_class_features(self)

    def choose_race(self, race_name):
        race = get_race(self, race_name)  # TODO: Make this input at
        # some point
        race.add_race_modifiers(self)

    def update(self):
        ### Modifiers
        attrs = self.attributes
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

        ### HP and Level calculation

        classes = self.classes

        level = 0
        HP = 0

        for class_name, class_obj in classes.items():
            level += class_obj.level
            if class_obj.base_class == True:
                HP += class_obj.hit_dice
            else:
                HP += class_obj.lvl_up_hp

        self.info.level = level

        HP += (level * attrs.CON.mod)
        self.stats.max_hp = int(HP)


char = character()

char.choose_class("Test")  # automatically run these on creating a character
char.choose_race("Half Orc")
char.update()

print("Done!")
