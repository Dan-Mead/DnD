"""Action Types:

Attacks (Weapons, Unarmed)
Combat: (Attack, Cast a Spell, Dash, Disengage, Dodge, Grapple, Help, Hide, Improvise, Ready, Search, Shove, Use an Object)
Bonus: Two weapon (if holding)
"""


class atk_option:

    def null(self, char):
        pass

    def ammunition(self, weapon):
        weapon, = weapon
        self.range = weapon.range
        # TODO: Ammo

    def finesse(self):
        self.mod_type = 'STR', 'DEX'

    def heavy(self, size):
        size, = size
        if size == 'Small':
            self.disadv = True

    def light(self):
        self.two_weapon_fighting = True

    def loading(self):
        self.round_limit = 1

    def reach_(self):
        self.reach = 10

    def special(self, weapon_name):
        name, = weapon_name

        notes = {'Lance': 'You have disadvantage when you use a lance to '
                          'Attack a target within 5 feet of you. Also, '
                          'a lance requires two hands to wield when you '
                          'aren’t mounted.',
                 'Net': 'A Large or smaller creature hit by a net is '
                        'Restrained until it is freed. A net has no effect on '
                        'creatures that are formless, or creatures that are '
                        'Huge or larger. A creature can use its action to '
                        'make a DC 10 Strength check, freeing itself or '
                        'another creature within its reach on a success. '
                        'Dealing 5 slashing damage to the net (AC 10) also '
                        'frees the creature without harming it, ending the '
                        'effect and destroying the net. When you use an '
                        'action, Bonus Action, or Reaction to Attack with a '
                        'net, you can make only one Attack regardless of the '
                        'number of attacks you can normally make. '
                 }
        self.note = notes[name]

    def thrown(self, weapon):
        weapon, = weapon
        self.range = weapon.range

    def two_handed(self, hands):
        hands, = hands
        if hands < 2:
            self.can_attack = False

    def versatile(self, hands):
        hands, = hands
        if hands == 2:
            self.dmg = (self.dmg[0], self.dmg[1] + 2)

    def __init__(self, char, weapon):

        ### Initialise

        self.can_attack = True

        if weapon.weapon_type[0] in char.proficiencies.weapons.set:
            self.prof = True
        else:
            self.prof = False

        if weapon.weapon_type[1] == 'Melee':
            self.mod_type = 'STR'
        elif weapon.weapon_type[1] == 'Ranged':
            self.mod_type = 'DEX'

        self.disadv = False
        self.round_limit = None
        self.reach = 5
        self.dmg = weapon.dmg
        self.dmg_type = weapon.dmg_type
        self.two_weapon_fighting = False

        properties = {'Ammunition': (self.ammunition, weapon),
                      'Finesse': (self.finesse,),
                      'Heavy': (self.heavy, char.stats.size.current),
                      'Light': (self.light,),
                      'Loading': (self.loading,),
                      'Reach': (self.reach_,),
                      'Special': (self.special, weapon.name),
                      'Thrown': (self.thrown, weapon),
                      'Two-handed': (
                          self.two_handed, char.wielded[weapon.name]['handed']),
                      'Versatile': (
                          self.versatile, char.wielded[weapon.name]['handed'])
                      }

        for property, values in properties.items():
            if property in weapon.properties:
                func = values[0]
                if len(values) > 1:
                    args = values[1:]
                    func(args)
                else:
                    func()

        print()

    def attack(self):
        print("Bonk!", self.dmg, "damage.")

class unarmed_strike(atk_option):
    def __init__(self, char):
        self.can_attack = True
        self.prof = True
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

