from addicted import Dict

from glossary import skills_dict, attrs
from races import get_race
from classes import get_class


def create_character():
    self = Dict()

    self.info.update({'alignment': None,
                      'level': None,
                      'fore_name': None,
                      'middle_name': None,
                      'family_name': None,
                      'race': None,
                      'size': Dict({'race': None, 'temp': None}),
                      'speed': Dict({'race': None, 'mod': None})
                      })

    self.profficiencies.update({'languages': Dict(),
                                'armor': Dict(),
                                'weapons': Dict({"Base": ["Unarmed"]}),
                                'tools': Dict(),
                                'other': Dict()
                                })

    self.bio.update({'faith': None
                     })

    self.stats.update({'max_hp': None,
                       'current_hp': None,
                       'armour_class': None,
                       'defences': None,
                       'conditions': None})

    self.actions.update({'actions': Dict(),
                         'bonus': Dict(),
                         'attack': Dict(),
                         'reaction': Dict()})

    self.attributes.update({attr: Dict({'base': None,
                                        'override': None})
                            for attr in attrs})

    self.saving_throws.update({attr: Dict({'mod': None,
                                           'override': None,
                                           'prof': False})
                               for attr in attrs})

    self.skills.update({skill: Dict({'name': skills_dict[skill][0],
                                     'attr': skills_dict[skill][1],
                                     'prof': False})
                        for skill in skills_dict})

    self.role_play.update(Dict())

    self.feats.update(Dict())

    self.features.update(Dict())

    return self


def choose_class(character, class_choice):
    starting_class = get_class(char, class_choice)
    starting_class.add_class_features(character)


def choose_race(character, race_name):
    race = get_race(character, race_name)  # TODO: Make this input at some point
    race.add_race_modifiers(character)


char = create_character()

choose_class(char, "Paladin")

choose_race(char, "Human Variant")

print("Done!")
