"""Action Types:

Attacks (Weapons, Unarmed)
Combat: (Attack, Cast a Spell, Dash, Disengage, Dodge, Grapple, Help, Hide, Improvise, Ready, Search, Shove, Use an Object)
Bonus: Two weapon (if holding)
"""
import textwrap


class atk_option:

    def null(self, char):
        pass

    def ammunition(self, weapon):
        weapon, = weapon
        self.range = weapon.range

    def finesse(self):
        self.attr = 'STR', 'DEX'

    def heavy(self, size):
        size, = size
        if size == 'Small':
            self.disadv += ['Small using heavy weapon']

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
            self.dmg_roll = (self.dmg_roll[0], self.dmg_roll[1] + 2)

    def __init__(self, char, weapon):

        ### Initialise

        self.can_attack = True

        if weapon.weapon_type[0] in char.proficiencies.weapons.set:
            self.prof = True
        else:
            self.prof = False

        if weapon.weapon_type[1] == 'Melee':
            self.attr = ('STR',)
        elif weapon.weapon_type[1] == 'Ranged':
            self.attr = ('DEX',)

        self.disadv = []
        self.round_limit = None
        self.reach = 5
        self.dmg_roll = weapon.dmg
        self.dmg_mod = 0
        self.dmg_type = weapon.dmg_type
        self.two_weapon_fighting = False

        properties = {'Ammunition': (self.ammunition, weapon),
                      'Finesse': (self.finesse,),
                      'Heavy': (self.heavy, char.data.size.current),
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
            if property in weapon.add_properties:
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
        self.attr = ('STR',)
        self.disadv = []
        self.round_limit = None
        self.reach = 5
        self.dmg_roll = None
        self.dmg_mod = 1
        self.dmg_type = 'Bludgeoning'

def attack_list(self):
    """ This is a fucking mess but what do you expect from trying to format strings.
    Prime candidate for refactoring."""

    print('\nAttack options:',
          f'\nNumber of attacks per round/action: {self.data.attacks_per_turn}\n')

    atk_rows = {}
    atk_cats = {}

    headers = {'names': 'Attack',
               'range': 'Reach (Range)',
               'atk': 'Hit Roll',
               'dmg': 'Damage Roll'
               }

    note = []

    for option, values in self.actions.attacks.items():
        if values.can_attack == True:
            atk_rows[option] = {'range': [],
                                'atk': [],
                                'dmg': []
                                }

            try:
                reach = (getattr(values, 'reach'),)
            except:
                pass
            else:
                atk_rows[option]['range'] += reach

            try:
                range = (getattr(values, 'range'),)
            except:
                pass
            else:
                atk_rows[option]['range'] += range

            atk_rows[option]['range'] = str(atk_rows[option]['range'])[1:-1]

            # Assume you'd want to use max. Can separate out if not, for some reason.
            roll_val = max([self.attributes[attr].mod for attr in values.attr])

            atk = f'1d20 + {roll_val + values.prof * self.data.proficiency}'

            if values.disadv:
                atk = f'{atk} (Disadvantage)'

            atk_rows[option]['atk'] = atk

            dmg = f'{roll_val + values.dmg_mod} {values.dmg_type}'

            if values.dmg_roll:
                dmg = f'{values.dmg_roll[0]}d{values.dmg_roll[1]} + {dmg}'

            atk_rows[option]['dmg'] = dmg

            try:
                if len(option) > atk_cats['names']:
                    atk_cats['names'] = len(option)
            except:
                atk_cats['names'] = max([len(option), len(headers['names'])])

            for key in atk_rows[option].keys():
                length = len(atk_rows[option][key])
                try:
                    if length > atk_cats[key]:
                        atk_cats[key] = length
                except:
                    atk_cats[key] = max([length, len(headers[key])])

            if hasattr(values, 'note'):
                note += [values.note]

    header = f'{headers["names"]:>{atk_cats["names"]}} | ' \
             f'{headers["range"]:^{atk_cats["range"]}} | ' \
             f'{headers["atk"]:^{atk_cats["atk"]}} | ' \
             f'{headers["dmg"]:^{atk_cats["dmg"]}}'

    header_len = len(header)
    atks = []
    for atk, vals in atk_rows.items():
        row = (f'{atk:>{atk_cats["names"]}} | '
               f'{vals["range"]:^{atk_cats["range"]}} | '
               f'{vals["atk"]:^{atk_cats["atk"]}} | '
               f'{vals["dmg"]:^{atk_cats["dmg"]}}')
        atks += [row]
        if len(row) > header_len:
            header_len = len(row)

    print(header)
    print(header_len * '-')
    for atk in atks: print(atk)

    print()

    if note:
        for comment in note: print(textwrap.fill(comment, width=80))


class shove:
    def __init__(self):
        self.desc = [
            "Using the Attack action, you can make a Special melee Attack to "
            "shove a creature, either to knock it prone or push it away from "
            "you. If you’re able to make multiple attacks with the Attack "
            "action, this Attack replaces one of them.",
            "The target must be no more than one size larger than you and "
            "must be within your reach. Instead of Making an Attack roll, "
            "you make a Strength (Athletics) check contested by the target’s "
            "Strength (Athletics) or Dexterity (Acrobatics) check (the target "
            "chooses the ability to use). If you win the contest, you either "
            "knock the target prone or push it 5 feet away from you."]


class limited_action:
    def __init__(self, desc, limit, reset):

        self.desc = desc
        self.max_uses = limit
        self.reset = reset
        self.current_uses = 0

    def use(self):
        if self.current_uses < self.max_uses:
            self.current_uses += 1
            print(self.desc)
            print(f'{self.current_uses}/{self.max_uses} uses')
        else:
            print("Not enough uses remaining!")
