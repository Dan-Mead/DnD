import numpy as np
from addict import Dict

from classes import get_class
from glossary import skills_dict, attrs
from helper_functions import mod_calc
from races import get_race


class character:

    def __init__(self, class_choice, race_choice):

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
                           'proficiency': None,
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

        self.saving_throws = Dict({attr: Dict({'val': None,
                                               'override': None,
                                               'prof': False})
                                   for attr in attrs})

        self.proficiencies = Dict({'languages': Dict(),
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

        self.choose_class(class_choice)
        self.choose_race(race_choice)

    def choose_class(self, class_choice):
        starting_class = get_class(self, class_choice)
        starting_class.add_class_features(self)

    def choose_race(self, race_name):
        race = get_race(self, race_name)
        race.add_race_modifiers(self)

    def update(self):

        ### Level calculation

        classes = self.classes

        level = 0
        for class_obj in classes.values():
            level += class_obj.level
        self.info.level = level

        ### Proficiency

        self.stats.proficiency = int(np.ceil(level / 4) + 1)

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
            attrs[attr_name].mod = int(mod_calc(total))

        ### Skills and saving throws

        skills = self.skills

        for skill in skills.values():
            ## Currently no systematic modifiers. Just get mod and add proff.

            skill['val'] = attrs[skill['attr']]['mod'] \
                            + self.stats.proficiency * skill['prof']

        saves = self.saving_throws

        for save_name, save in saves.items():
            if save.override:
                save.val = save.override
            else:
                save.val = attrs[save_name].mod \
                                + self.stats.proficiency * save['prof']


        ### HP

        HP = 0

        for class_obj in classes.values():
            if class_obj.base_class:
                HP += class_obj.hit_dice
            else:
                HP += class_obj.lvl_up_hp

        HP += (level * attrs.CON.mod)
        self.stats.max_hp = int(HP)


class_choice = "Test"
race_choice = "Half Orc"

char = character(class_choice, race_choice)
char.update()

print("Done!")
