"""Action Types:

Attacks (Weapons, Unarmed)
Combat: (Attack, Cast a Spell, Dash, Disengage, Dodge, Grapple, Help, Hide, Improvise, Ready, Search, Shove, Use an Object)
Bonus: Two weapon (if holding)
"""

class unarmed_strike:
    def __init__(self, char):

        self.prof = True
        self.attack_type = 'Melee'
        self.reach = 5
        self.dmg = 1 + char.attributes.STR.mod
        self.dmg_type = 'Bludgeoning'

    def attack(self):
        print("Bash")
        print(self.dmg, "damage done")

def attack(self):

    attacks = {'Unarmed Strike' : unarmed_strike(self)}

    print(attacks['Unarmed Strike'].attack())

