from glossary import *
import helper_functions as f
from types import SimpleNamespace

class MT():
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

class Bio:
    def __init__(self):
        self.faith = None
        self.languages = SimpleNamespace()


class Attributes:

    class Attribute:
        def __init__(self):
            self.base = None
            self.override = None

    def __init__(self):
        for atr in stats_str:
            setattr(self, atr, self.Attribute())


class skills:
    class skill:
        def __init__(self, name, attr):
            self.name = name
            self.attr = attr
            self.prof = False

    def __init__(self):
        for key in skills_dict:
            setattr(self, key, self.skill(*skills_dict[key]))

def Race(self, race_name):

    if race_name == "Human":
        self.info.size.base = "Medium"
        self.info.speed.base = 30
        self.attributes.race = [(STR, +1), (DEX, +1), (CON, +1), (INT, +1), (WIS, +1), (CHA, +1)]
        languages = ["Common"]
        second_language = f.choose_language("Choose second language: ", languages)
        self.bio.languages.race = languages + second_language

    elif race_name == "Human Variant":
        self.info.size.base = "Medium"
        self.info.speed.base = 30
        score_1 = f.choose_stat("Choose first ability score to increase (STR, DEX, etc.): ")
        score_2 = f.choose_stat("Choose second ability score to increase (STR, DEX, etc.): ", [score_1])
        self.attributes.race = [(score_1, +1),(score_2,+1)]
        languages = ["Common"]
        second_language = f.choose_language("Choose second language: ", languages)
        self.bio.languages.race = languages + second_language
        
    elif race_name == "Test":
        race_skill = f.choose_skill("Choose skill profficiency: ", self.skills)
        print(race_skill)
        
class PC:

    def __init__(self):
        self.info = Info()
        self.bio = Bio()
        self.attributes = Attributes()
        self.skills = skills()
        Race(self, "Test")



char = PC()

print("Done")