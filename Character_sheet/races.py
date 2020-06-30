import helper_functions as f
from glossary import *

class Race():

    def add_race_modifiers(self, char):
        
        race_key = {
            'race_name' : ['info'],
            'size' : ['info', 'size'],
            'speed' : ['info', 'speed'],
            'languages': ['profficiencies', 'languages'],
            'attributes' : ['attributes'],
            'skills' : ['skills'],
            'feats' : ['feats'],
            'features' : ['features']}

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
                from features import feature_list
                for feature in self.features:
                    # char.features['race'] += [feature]
                    char.features['race'].update({feature : feature_list[feature]()})

    def remove_race_modifiers(self):
        pass

def get_race(char, race_choice):

    ## TODO: Make this input at some point

    race_list = {'Human' : Human_Base,
                'Human Variant' : Human_Variant,
                'Half-Orc' : Half_Orc,
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

    ## TODO: Possibly need to include adding scores other than 1.

    attrs_list = []
    for n in range(num_attr):
        attrs_list.append(f.choose_stat("Choose " + ordinals[n].lower() + " ability score to increase,", attrs_list))

    return list(zip(attrs_list, [1] * len(attrs_list)))

def add_skill(char_skills, allowed, num_skills):

    skills_list = []
    
    profficient = [skill for skill in char_skills if char_skills[skill]['prof'] == True]

    ## TODO: If only allowed some, list here

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

class Human_Base(Human):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = [(attr, 1) for attr in attrs]
 
class Human_Variant(Human):
    def __init__(self, char):
        super().__init__(char)
        self.attributes = add_attributes(attrs, 2)
        self.skills = add_skill(char.skills, skills_dict.keys(), 1)
        self.feats = add_feat(char, 1)

class Half_Orc(Race):
    def __init__(self,char):
        self.race_name = "Half-Orc"
        self.size = "Medium"
        self.speed = 30
        self.attributes = [("STR", 2), ("CON", 1), ("INT", -2)]
        self.features = ["Darkvision", "Relentless Endurance", "Savage Attacks"]
        self.skills = ["intimidation"]
        self.languages = ["Common", "Orc"]

class Test(Race):
        def __init__(self, char):
            self.feats = add_feat(char, 1)