"""Action Types:

Attacks (Weapons, Unarmed)
Combat: (Attack, Cast a Spell, Dash, Disengage, Dodge, Grapple, Help, Hide, Improvise, Ready, Search, Shove, Use an Object)
Bonus: Two weapon (if holding)
"""


class atk_option:
    def __init__(self, char, weapon):
        self.prof
        self.mod_type
        self.disadv
        self.round_limit
        self.reach
        self.dmg
        self.dmg_type

    def attack(self):
        print("Bonk!", self.dmg, "damage.")

class unarmed_strike(atk_option):
    def __init__(self, char):

        self.prof = True
        self.attack_type = 'Melee'
        self.disadv = False
        self.round_limit = None
        self.reach = 5
        self.dmg = 1 + char.attributes.STR.mod
        self.dmg_type = 'Bludgeoning'





# def attack(self):
#
#     attacks = {'Unarmed Strike' : unarmed_strike(self)}
#
#     print(attacks['Unarmed Strike'].attack())

