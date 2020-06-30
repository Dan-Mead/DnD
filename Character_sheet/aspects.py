from addict import Dict
from glossary import *
import helper_functions as f
from races import get_race

def create_character():

        self = Dict()

        self.info.update({'alignment' : None, 
                        'level' : None, 
                        'fore_name' : None,
                        'middle_name' : None,
                        'family_name' : None,
                        'race' : None,
                        'size' : Dict({'race' : None, 'temp' : None}),
                        'speed' : Dict({'race' : None, 'mod' : None})
                        })

        self.profficiencies.update({'languages' : Dict(), 
                        'armor' : Dict(),
                        'weapons' : Dict(),
                        'tools' : Dict(),
                        'other' : Dict()
                        })

        self.bio.update({'faith' : None
                        })

        self.stats.update({'max_hp' : None,
                        'current_hp' : None,
                        'armour_class' : None})

        self.actions.update({'actions' : Dict(),
                        'bonus' : Dict(),
                        'attack' : Dict(),
                        'reaction' : Dict()})

        self.attributes.update({attr : Dict({'base' : None, 
                                        'override' : None}) 
                                        for attr in attrs})

        self.saving_throws.update({attr : Dict({'mod' : None, 
                                                'override' : None, 
                                                'prof' : False}) 
                                                for attr in attrs})

        self.skills.update({skill : Dict({'name' : skills_dict[skill][0],
                                        'attr' : skills_dict[skill][1],
                                        'prof' : False})
                                        for skill in skills_dict})

        self.role_play.update(Dict())

        self.feats.update(Dict())

        self.features.update(Dict())

        return self

def choose_class(character, class_choice):
        pass

def choose_race(character, race_name):
        
        race = get_race(character, race_name)
        race.add_race_modifiers(char)
        
        return race

char = create_character()

char.race = choose_race(char, "Half-Orc")

print("Done!")
