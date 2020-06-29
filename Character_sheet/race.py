import helper_functions as f
from glossary import *

class Race():

    # def __init__(self):
        # pass

    def add_race_modifiers(self, character):
        
        race_key = {
            'race_name' : ['info'],
            'size' : ['info', 'size'],
            'speed' : ['info', 'speed'],
            'languages': ['profficiencies', 'languages'],
            'attributes' : ['attributes'],
            'skills' : ['skills'],
            'feats' : ['feats']}

        

        # for key in self.traits:
            # value = (self.traits[key])
            # print(race_key[key])
            # print(value) 

            # f.LDK(character, race_key[key]))


    def remove_race_modifiers(self):
        pass

def get_race(char, race_choice):

    ### Make this input at some point

    race_list = {'Human' : Human,
                'Human Variant' : Human_variant,
                'Test' : Test}

    race = race_list[race_choice](char)
    
    return race

def add_language(char_languages, default, num_lang):

    lang_list = []
    lang_list.append(default)
    for n in range(num_lang):
        new_lang = f.choose_language("Choose " + ordinals[len(lang_list)].lower() + " language,", [default] + list(char_languages.values()))
        lang_list.append(new_lang)

    return list(filter(None, lang_list))

def add_attributes(allowed, num_attr):

    ### Possibly need to include adding scores other than 1.

    attrs_list = []
    for n in range(num_attr):
        attrs_list.append(f.choose_stat("Choose " + ordinals[n].lower() + " ability score to increase,", attrs_list))

    return list(zip(attrs_list, [1] * len(attrs_list)))

def add_skill(char_skills, allowed, num_skills):

    skills_list = []
    
    profficient = [skill for skill in char_skills if char_skills[skill]['prof'] == True]

    ## If only allowed some, list here

    for n in range(num_skills):
        skills_list.append(f.choose_skill("Choose " + ordinals[n].lower() + " skill to gain profficiency in,", profficient))

    return skills_list

def add_feat(char, num_feats):

    feats_list = []

    for n in range(num_feats):
        feats_list.append(f.choose_feat("Choose a feat,", char))

    return feats_list



class Human(Race):
        def __init__(self, char):
            self.race_name = "Human"
            self.size = 'Medium'
            self.speed = 30
            self.languages = add_language(char.profficiencies.languages, 'Common', 1)
            self.attributes = [(attr, 1) for attr in attrs]

class Human_variant(Race):
        def __init__(self, char):
            self.race_name = "Human"
            self.size = 'Medium'
            self.speed = 30
            self.languages = add_language(char.profficiencies.languages, 'Common', 1)
            self.attributes = add_attributes(attrs, 2)
            self.skills = add_skill(char.skills, skills_dict.keys(), 1)
            self.feats = add_feat(char, 1)

class Test(Race):
        def __init__(self, char):
            self.feats = add_feat(char, 1)