from Character_Sheet.reference.equipment import *
from Character_Sheet.reference.skills_and_attributes import *


class CharacterClass:
    pass


class Paladin(CharacterClass):

    name = "Paladin"
    desc = "Paladin desc here"

    def base_features(self):
        self.hit_die = 10
        self.lvl_up_hp = 6
        self.armour_proficiencies = (Light, Medium, Heavy, Shields)
        self.weapon_proficiencies = (Simple, Martial)
        self.tool_proficiencies = (None,)
        self.saving_throws = (WIS, CHA)
        self.skills = ("choose", "choose")
        self.valid_skills = (Athletics, Insight, Intimidation, Medicine, Persuasion, Religion)
        self.equipment = (
            ([(Martial, 1), (Shield, 1)],
             [(Martial, 2)]
             ),
            ([(Javelin, 5)],
             [((Simple, Melee), 1)]
             ),
            ([(PriestPack, 1)],
             [(ExplorerPack, 1)]
             ),
            ([(ChainMail, 1)]),
            ([(HolySymbol, 1)])
        )


class Rogue(CharacterClass):

    name = "Rogue"
    desc = "Rogue Desc Here"

    def __init__(self):
        pass

    def base_features(self):
        self.hit_die = 8
        self.lvl_up_hp = 5
        self.armour_proficiencies = (Light,)
        self.weapon_proficiencies = (Simple, HandCrossbow, Longsword, Rapier, Shortsword)
        self.tool_proficiencies = (Thieves,)
        self.saving_throws = (DEX, INT)
        self.skills = ("choose", "choose", "choose", "choose")
        self.valid_skills = (
        Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion,
        SleightOfHand, Stealth)
        self.equipment = (
            ([(Rapier, 1)],
             [(Shortsword, 1)]
             ),
            ([(Shortbow, 1), (Arrow, 20)],
             [(Shortsword, 1)]
             ),
            ([(BurglarPack, 1)],
             [(DungeoneerPack, 1)],
             [(ExplorerPack, 1)]
             ),
            ([(LeatherArmour, 1)]),
            ([(Dagger, 2)]),
            ([(ThievesTools, 1)])
        )

class_list = {class_.name: class_ for class_ in CharacterClass.__subclasses__()}

if __name__ == '__main__':
    pass
