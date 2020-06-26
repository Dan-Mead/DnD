import helper_functions as f
from glossary import *

class Race():

    def __init__(self, race_choice):
        self.traits = race_choice

    def add_race_modifiers(self, character):
        
        race_key = {
            'race_name' : ['info'],
            'size' : ['info', 'size'],
            'speed' : ['info', 'speed'],
            'languages': ['profficiencies', 'languages'],
            'attributes' : ['attributes'],
            'skills' : ['skills'],
            'feats' : ['feats']}

        

        for key in self.traits:
            value = (self.traits[key])
            # print(race_key[key])
            # print(value)

            f.LDK(character, race_key[key]))


    def remove_race_modifiers(self):
        pass

def get_race(race_name):

    # Get information from dictionary

    race_choice = race_list[race_name]

    race = Race(race_choice) ## must fully create here

    return race

def add_language(self, default, num_lang):
    if default:
            self.languages += default
    for n in range(num_lang):                
            new_lang = f.choose_language("Choose " + ordinals[n+1].lower() + " language,", self.profficiencies.languages)
            if new_lang:
                    self.profficiencies.languages.race += [new_lang]

human = {
        'race_name' : "Human",
        'size' : 'Medium',
        'speed' : 30,
        'languages' : ['Common', 'choose'],
        'attributes' : [(attr, 1) for attr in attrs]}

human_variant = {
        'race_name' : "Human",
        'size' : 'Medium',
        'speed' : 30,
        'languages' : ['Common', 'choose'],
        'attributes' : [('choose', 1), ('choose', 1)],
        'skills' : ['choose'],
        'feats' : ['choose']}

race_list = {"Human" : human, 
            "Human Variant" : human_variant}

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
