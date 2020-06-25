from glossary import *
import helper_functions as f
from types import SimpleNamespace
from feats import feats

class Empty:
    def __init__(self):
        pass

class Info:
    def __init__(self):
        self.name = None
        self.race = None
        self.level = None
        self.alignment = None
        self.size = SimpleNamespace(temp = None)
        self.speed = SimpleNamespace(mod = None)

class Profficiencies: 
    def __init__(self):
        self.languages = SimpleNamespace()
        self.armor = SimpleNamespace()
        self.weapon = SimpleNamespace()

class Bio:
    def __init__(self):
        self.faith = None

class Stats:
    def __init__(self):
        self.max_hp = None
        self.current_hp = None
        self.armor_class = SimpleNamespace(worn = None)

class Actions:
    def __init__(self):
        self.actions = SimpleNamespace()
        self.bonus = SimpleNamespace()
        self.attack = SimpleNamespace()
        self.reaction = SimpleNamespace()
        ## Note will probably want flags for limited use and combat actions

class Attributes:

    class Attribute:
        def __init__(self):
            self.base = None
            self.override = None

    def __init__(self):
        for attr in attrs.keys():
            setattr(self, attr, self.Attribute())

class Saving_Throws:
    def __init__(self):
        for attr in attrs.keys():
            setattr(self, attr, SimpleNamespace(prof = False, note = SimpleNamespace()))

class skills:
    class skill:
        def __init__(self, name, attr):
            self.name = name
            self.attr = attr
            self.prof = False
            self.note = SimpleNamespace()

    def __init__(self):
        for key in skills_dict:
            setattr(self, key, self.skill(*skills_dict[key]))

def Race(self, race_name):

    if race_name == "Human":

        # Base Traits
        self.info.size.base = "Medium"
        self.info.speed.base = 30

        # +1 to all attributes
        for attr in attrs.keys():
            f.rsetattr(self.attributes, attr+".race", +1)

        # Common + 1 language
        languages = "Common"
        second_language = f.choose_language("Choose second language,", languages)
        self.profficiencies.languages.race = languages, second_language

    elif race_name == "Human Variant":

        # Base Traits
        self.info.size.base = "Medium"
        self.info.speed.base = 30

        # +1 to 2 attributes
        score_1 = f.choose_stat("Choose first ability score to increase,")
        score_2 = f.choose_stat("Choose second ability score to increase,", [score_1])
        f.rsetattr(self.attributes, score_1+".race", +1)
        f.rsetattr(self.attributes, score_2+".race", +1)        

        # Common + 1 language
        languages = "Common"
        second_language = f.choose_language("Choose second language,", languages)
        self.profficiencies.languages.race = languages,  second_language

        # 1 skill profficiency
        race_skill = f.choose_skill("Choose skill profficiency,", self.skills)
        f.rsetattr(self.skills, race_skill+".prof", True)

        # 1 Feat
        new_feat = f.choose_feat("Choose a new feat,", self)
        f.add_feat(self, "race", new_feat)
        
    elif race_name == "Test":
        pass
        # new_feat = f.choose_feat("Choose a new feat,", self)
        # f.add_feat(self, "race", new_feat)

        
class PC:

    def __init__(self):
        
        self.info = Info()
        self.bio = Bio()
        self.profficiencies = Profficiencies()
        self.saving_throws = Saving_Throws()
        self.feats = Empty()
        self.actions = Actions()
        self.role_play = Empty()        
        self.stats = Stats()
        self.attributes = Attributes()
        self.skills = skills()
        Race(self, "Test")
        


char = PC()

# char.profficiencies.armor.race = "Heavy", "Medium"
# char.profficiencies.armor.p_class = "Light", "Medium", "Heavy"

print("Done")