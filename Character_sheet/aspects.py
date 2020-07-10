import numpy as np
from addict import Dict

from classes import get_class
from glossary import skills_dict, attrs
from helper_functions import mod_calc, simple_choice
from races import get_race


class character:

    def __init__(self, class_choice, race_choice):

        self.info = Dict({'alignment': None,
                          'level': None,
                          'fore_name': None,
                          'middle_name': None,
                          'family_name': None,
                          'race': None
                          })

        self.bio = Dict({'faith': None
                         })

        self.stats = Dict({'max_hp': None,
                           'current_hp': None,
                           'armour_class': Dict({'value': None,
                                                 'special': None
                                                 }),
                           'proficiency': None,
                           'defences': None,
                           'conditions': None,
                           'size': Dict({'race': None, 'temp': None}),
                           'speed': Dict({'race': None, 'mod': None}),
                           'senses': Dict({'perception': None,
                                           'investigation': None,
                                           'insight': None}),
                           'initiative': False
                           })

        self.attributes = Dict({attr: Dict({'base': 10,
                                            'stat' : None,
                                            'mod' : None,
                                            'override': None})
                                for attr in attrs})

        self.skills = Dict({skill: Dict({'name': skills_dict[skill][0],
                                         'attr': skills_dict[skill][1],
                                         'prof': False})
                            for skill in skills_dict})

        self.saving_throws = Dict({attr: Dict({'val': None,
                                               'override': None,
                                               'prof': False})
                                   for attr in attrs})

        self.proficiencies = Dict({'languages': Dict(),
                                   'armor': Dict(),
                                   'weapons': Dict({"Base": ["Unarmed"]}),
                                   'tools': Dict(),
                                   'other': Dict()
                                   })

        self.actions = Dict({'actions': Dict(),
                             'bonus': Dict(),
                             'attack': Dict(),
                             'reaction': Dict()})

        self.feats = Dict()

        self.features = Dict()

        self.equipment = Dict()

        self.equipped = Dict()

        self.choose_class(class_choice)
        self.choose_race(race_choice)

    def choose_class(self, class_choice):
        starting_class = get_class(self, class_choice)
        starting_class.add_class_features(self)

    def choose_race(self, race_name):
        race = get_race(self, race_name)
        race.add_race_modifiers(self)

    def equip(self):

        equipment = self.equipment

        self.equipped = Dict({'Body': None,
                              'Right Hand': None,
                              'Left Hand': None,
                              'Shoulders': None,
                              'Feet': None})

        equippable = {}
        for item_name, item in equipment.items():
            if hasattr(item, 'equippable'):
                equippable[item_name] = [item.equippable, item.num]

        two_handed = None
        hands = 0
        for body_part in self.equipped:
            if not ('Hand' in body_part and two_handed):
                options = [item_name for item_name, item in equippable.items()
                           if item[0] in body_part and item[1] >= 1]
                if options:
                    options.insert(0, 'None')
                    valid_choice = False

                    while not valid_choice:
                        print(f"\nChoose item to equip ({body_part.lower()}):")
                        choice = simple_choice(options)

                        warning = None
                        eq = equipment[options[choice]]

                        if not choice:
                            pass
                        elif hasattr(eq, 'armor_type'):
                            if eq.armor_type not in self.proficiencies.armor.set:
                                warning = 'Not proficient in armor type!'
                            if self.attributes.STR.stat < eq.req:
                                warning = 'Strength too low for armor!'
                        elif hasattr(eq, 'weapon_type'):
                            if eq.weapon_type[0] not in self.proficiencies.weapons.set:
                                warning = 'Not proficient in weapon type!'

                        if warning:
                            print('Warning!', warning)
                            answer = input(
                                'Would you like to choose another option? Y/N').lower()
                            if answer in 'yes':
                                pass
                            else:
                                valid_choice = True
                        else:
                            valid_choice = True

                    if choice:
                        choice = options[choice]

                        # Awkward shit to do with 2-handed equipment.

                        if hands == 0 and \
                                (hasattr(eq, 'properties')
                                    and 'Versatile' in eq.properties):
                            wield = None
                            while wield not in ['y', 'yes', 'n', 'no']:
                                wield = input(f'Wield {choice.lower()} two-handed? (Y/N)').lower()
                                if ('y' or 'yes') in wield:
                                    two_handed = eq
                                    equippable[choice][1] -= 1
                                elif ('n' or 'no') in wield:
                                    self.equipped[body_part] = eq
                                    equippable[choice][1] -= 1
                                else:
                                    wield = input(
                                        f'Input error. Wield {choice.lower()} two-handed? (Y/N)').lower()
                        else:
                            self.equipped[body_part] = eq
                            equippable[choice][1] -= 1
                    if 'Hand' in body_part:
                        hands += 1
        if two_handed:
            self.equipped['Hands'] = two_handed

        self.equipped = Dict(
            {part: item for part, item in self.equipped.items() if item})

        ## Check for effects

        for item in self.equipped.values():
            if hasattr(item, 'effects'):
                for effect in item.effects:
                    effect.add_effect(self)

    def update(self):

        ### Level calculation

        classes = self.classes

        level = 0
        for class_obj in classes.values():
            level += class_obj.level
        self.info.level = level

        ### Proficiency

        self.stats.proficiency = int(np.ceil(level / 4) + 1)

        ### Modifiers

        attrs = self.attributes
        for attr_name, attr in attrs.items():
            attr.stat = 0
            if attr.override:
                attr.stat = attr.override
                break
            else:
                for mod_name, mod_val in attr.items():
                    if mod_name not in ['override', 'mod', 'stat']:
                        attr.stat += sum([mod_val])
                attr.mod = int(mod_calc(attr.stat))

        ### Skills and saving throws

        skills = self.skills

        for skill in skills.values():
            skill['val'] = attrs[skill['attr']]['mod'] \
                           + self.stats.proficiency * skill['prof']
            for mod_name, mod_val in skill.items():
                if not mod_name in ['val', 'name', 'attr', 'prof']:
                    skill['val'] += sum(mod_val)

        saves = self.saving_throws

        for save_name, save in saves.items():
            if save.override:
                save.val = save.override
            else:
                save.val = attrs[save_name].mod + self.stats.proficiency * save[
                    'prof']

                for mod_name, mod_val in save.items():
                    if not mod_name in ['val', 'override', 'prof']:
                        save.val += sum(mod_val)

        ### HP #TODO: Temp HP?

        HP = 0

        for class_obj in classes.values():
            if class_obj.base_class:
                HP += class_obj.hit_dice
            else:
                HP += class_obj.lvl_up_hp

        HP += (level * attrs.CON.mod)
        self.stats.max_hp = int(HP)

        ### Passive senses

        senses = self.stats.senses

        senses.perception = 10 + attrs.WIS.mod
        senses.investigation = 10 + attrs.INT.mod
        senses.insight = 10 + attrs.WIS.mod

        ### AC calc

        stats = self.stats
        armoured = False

        AC = 0

        if not stats.armour_class.special:  ## special types to do later
            for item in self.equipped.values():
                if hasattr(item, 'AC'):
                    armor_type = item.armor_type
                    if armor_type == 'Heavy':
                        AC += item.AC
                        armoured = True
                    elif armor_type == 'Medium':
                        dex_mod = self.attributes['DEX']['mod']
                        if dex_mod > 2:
                            dex_mod = 2
                        AC += item.AC + dex_mod
                        armoured = True
                    elif armor_type == 'Light':
                        AC += item.AC + self.attributes['DEX']['mod']
                        armoured = True
                    elif armor_type == 'Shield':
                        AC += 2

        for mod_name, mod_val in stats.armour_class.items():
            if not mod_name in ['value',
                                'special']:  # recall overrides etc here
                AC += sum(mod_val)

        if not armoured:
            AC += 10 + self.attributes['DEX']['mod']

        stats.armour_class['value'] = AC

        ### Update profficiencies

        for prof in self.proficiencies:
            prof_set = list(set([pro for pros in self.proficiencies[prof].values() for pro in pros]))
            self.proficiencies[prof].set = prof_set


class_choice = "Test"
race_choice = "Half Orc"

char = character(class_choice, race_choice)
char.update()

from items import get_item

char.equipment.update(
    {'Cloak of Protection': get_item('Cloak of Protection', 1)})

char.equip()
char.update()

print("Done!")
