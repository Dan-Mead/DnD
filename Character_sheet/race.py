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

    race_list = {'Human' : Human,
                'Human Variant' : Human_variant}

    race = race_list[race_choice](char)
    
    return race

def add_language(char, default, num_lang):

    lang_list = []
    lang_list.append(default)
    for n in range(num_lang):
        new_lang = f.choose_language("Choose " + ordinals[len(lang_list)].lower() + " language,", [default] + list(char.profficiencies.languages.values()))
        lang_list.append(new_lang)

    return list(filter(None, lang_list))

def add_attributes(allowed, num_attr):

    attrs_list = []

    for n in range(num_attr):
        attrs_list.append(f.choose_stat("Choose " + ordinals[n].lower() + " ability score to increase,", attrs_list))

    return attrs_list, [1] * len(attrs_list)
    

class Human(Race):
        def __init__(self, char):
            self.race_name = "Human"
            self.size = 'Medium'
            self.speed = 30
            self.languages = add_language(char, 'Common', 1)
            self.attributes = [(attr, 1) for attr in attrs]

class Human_variant(Race):
        def __init__(self, char):
            self.race_name = "Human"
            self.size = 'Medium'
            self.speed = 30
            self.languages = add_language(char, 'Common', 1)
            self.attributes = list(zip(add_attributes(attrs, 2)))
            self.skills = ['choose']
            self.feats = ['choose']

# class Race_list:



# def Race(self, race_name):


#         if race_name == "Human":

#                 # Base Traits
#                 self.info.size.race = "Medium"
#                 self.info.speed.race = 30

#                 # +1 to all attributes
#                 for attr in self.attributes.keys():
#                         self.attributes[attr].update({'race' : 1})

#                 # Common + 1 language
#                 add_race_language(self, "Common", 1)
                
#         elif race_name == "Human Variant":

#                  # Base Traits
#                 self.info.size.race = "Medium"
#                 self.info.speed.race = 30

#                 # +1 to 2 attributes
#                 score_1 = f.choose_stat("Choose first ability score to increase,")
#                 score_2 = f.choose_stat("Choose second ability score to increase,", [score_1])
#                 self.attributes[score_1].update({'race' : 1})
#                 self.attributes[score_2].update({'race' : 1})
                
#                 # Common + 1 language
#                 add_race_language(self, "Common", 1)

#                 # 1 skill profficiency
#                 race_skill = f.choose_skill("Choose skill profficiency,", self.skills)
#                 f.rsetattr(self.skills, race_skill+".prof", True)

#                 # 1 Feat
#                 new_feat = f.choose_feat("Choose a new feat,", self)
#                 f.add_feat(self, "race", new_feat)
