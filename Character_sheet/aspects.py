import numpy as np
from addict import Dict

from actions import atk_option, unarmed_strike
from classes import get_class
from glossary import skills_dict, attrs, ordinals
from helper_functions import mod_calc, simple_choice, isclasstype, reset, \
    get_bases
from races import get_race


class character:

    def __init__(self):

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
                           'speed': Dict({'race': None}),
                           'senses': Dict({'perception': None,
                                           'investigation': None,
                                           'insight': None}),
                           'initiative': False,
                           'attacks_per_turn': 1,
                           'max_attuned': 3,
                           'attuned': Dict()
                           })

        self.attributes = Dict({attr: Dict({'base': 10,
                                            'stat': None,
                                            'mod': None,
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
                             'attacks': Dict(),
                             'reactions': Dict()})

        self.worn = Dict({'Body': None,
                          'Shoulders': None,
                          'Hands': None,
                          'Wrists': None,
                          'Head': None,
                          'Feet': None,
                          'Legs': None,
                          'Belt': None,
                          'Rings': None,
                          'Neck': None})

        self.wielded = Dict()

        self.feats = Dict()

        self.features = Dict()

        self.equipment = Dict()
        self.penalties = Dict()

        self.other = Dict({'dual_wield_requirement': 'Light',
                           'can_cast_spells': True,
                           })

    def choose_class(self, class_choice):
        starting_class = get_class(self, class_choice)
        starting_class.add_class_features(self)

    def choose_race(self, race_name):
        race = get_race(self, race_name)
        race.add_race_modifiers(self)

    def equip(self):
        equipment = self.equipment

        self.worn = reset(self.worn)

        equippable = {}
        for item_name, item in equipment.items():
            if hasattr(item, 'equippable') and not isclasstype(item, 'Weapon'):
                equippable[item_name] = [item.equippable, item.num]

        for body_part in self.worn:
            choices = [item_name for item_name, item in equippable.items()
                       if body_part in item[0] and item[1] >= 1]

            if choices:

                choices.insert(0, None)

                final_choice = False

                while not final_choice:
                    print(f"\nChoose item to equip ({body_part.lower()}):")
                    choice_num = simple_choice(choices)
                    choice = choices[choice_num]
                    if choice:
                        eq = equipment[choice]
                        warnings = []
                        penalties = []

                        if hasattr(eq, 'req') \
                                and eq.req \
                                and eq.req > self.attributes.STR.stat:
                            warnings += ['Strength too low for armour']
                            penalties += ['Armor STR']

                        if hasattr(eq, 'armor_type') \
                                and eq.armor_type not in self.proficiencies.armor.set:
                            warnings += [
                                f'Not proficient in armour type ({eq.armor_type})']
                            penalties += ['Armor Prof']

                        if not warnings:
                            final_choice = True
                        else:
                            warnings = [warning.lower() if n >= 1
                                        else warning for n, warning in
                                        enumerate(warnings)]
                            print('Warning!', " and ".join(warnings) + "!")
                            choose_again = input(
                                "Choose a different option? Y/N").lower()

                            if choose_again in 'no':
                                self.penalties.update({eq: list(penalties)})
                                final_choice = True
                            else:
                                pass
                    else:
                        final_choice = True

                if choice:
                    if body_part != 'Rings':
                        self.worn[body_part] = (eq.name, eq)

                    else:
                        self.worn[body_part] = Dict({eq.name: eq})

                    equippable[choice][1] -= 1

        for part, worn in self.worn.items():
            if worn:
                item_name, item = worn
                if hasattr(item, 'effects'):
                    if (hasattr(item,
                                'attunement') and item_name in self.stats.attuned.keys()) \
                            or not hasattr(item, 'attunement'):
                        for effect in item.effects:
                            effect.add_effect(self)
                if hasattr(item, 'components'):
                    for body_part, component in item.components.items():
                        if not self.worn[body_part]:
                            if body_part != 'Rings':
                                self.worn[body_part] = (component, None)
                            else:
                                self.worn[body_part] = {component: None}

        self.update()

    def wield(self):

        self.wielded = Dict()
        equipment = self.equipment

        equippable = {}

        for item_name, item in equipment.items():
            if hasattr(item,
                       'equippable') and item.equippable == 'Hand':  # covers 'other' items, may need changing in future.
                equippable[item_name] = [get_bases(item), item.num]
            if isclasstype(item, 'Weapon'):
                equippable[item_name] = [get_bases(item), item.weapon_type,
                                         item.properties, item.num]

        hands = 0

        while hands < 2:
            choices = [item_name for item_name, item in equippable.items()
                       if item[-1] >= 1]
            choices.insert(0, None)

            print(f"\nChoose {ordinals[hands].lower()} item to wield!")
            choice_num = simple_choice(choices)
            choice = choices[choice_num]

            if choice:
                if 'Weapon' in equippable[choice][0]:
                    if equippable[choice][1][
                        0] not in self.proficiencies.weapons.set:
                        print(
                            f'Warning! Not proficient with {equippable[choice][1][0].lower()} weapons!')
                        choose_again = input(
                            "Choose a different option? Y/N").lower()
                        if choose_again in 'no':
                            pass
                        else:
                            continue

                    if 'Versatile' in str(equippable[choice][2]) and hands == 0:
                        two_hand = input('Wield two-handed? Y/N').lower()
                        if two_hand in 'yes':
                            handed = 2
                        else:
                            handed = 1
                    else:
                        handed = 1

                    if 'Two-handed' in equippable[choice][2]:
                        if hands == 0:
                            two_hand = input('Wield two-handed? Y/N').lower()
                            if two_hand in 'yes':
                                handed = 2
                            else:
                                handed = 1
                                print(
                                    'Warning! Weapon requires two hands to attack')
                                choose_again = input(
                                    "Choose a different option? Y/N").lower()

                                if choose_again in 'no':
                                    handed = 1
                                else:
                                    continue

                        else:
                            print(
                                'Warning! Weapon requires two hands to attack')
                            choose_again = input(
                                "Choose a different option? Y/N").lower()

                            if choose_again in 'no':
                                handed = 1
                            else:
                                continue

                elif choice == 'Shield':
                    if 'Shield' in self.proficiencies.armor.set:
                        handed = 1
                    else:
                        print('Warning! Not proficient with Shields!')
                        choose_again = input(
                            "Choose a different option? Y/N").lower()

                        if choose_again in 'no':
                            self.penalties.update(
                                {equipment[choice]: ('Armor Prof')})
                            handed = 1
                        else:
                            continue

                equippable[choice][-1] -= 1
                self.wielded.update(Dict({choice: {'handed': handed,
                                                   'obj': equipment[choice]}}))
            else:
                handed = 1
                if not self.wielded and hands >= 1:
                    print('Why did you even bother?')

            hands += handed

        self.update()

    def attune(self):
        attuneable = {}
        self.stats.attuned = Dict()

        for name, eq in self.equipment.items():
            if hasattr(eq, 'attunement'):
                attuneable[name] = eq

        choices = [name for name in attuneable.keys()]
        choices.insert(0, None)
        while len(self.stats.attuned) < self.stats.max_attuned:
            if len(choices) > 1:
                print(
                    f"Choose items to attune. Currently {len(self.stats.attuned)}/{self.stats.max_attuned} chosen.")
                choice = simple_choice(choices)
                if choice:
                    self.stats.attuned[choices[choice]] = attuneable[
                        choices[choice]]
                del choices[choice]
            else:
                break
        self.update()

    def update(self, func=None):

        def levels():

            classes = self.classes

            level = 0
            for class_obj in classes.values():
                level += class_obj.level
            self.info.level = level

            self.stats.proficiency = int(np.ceil(level / 4) + 1)

        def modifiers():

            attrs = self.attributes
            for attr_name, attr in attrs.items():
                attr.stat = 0
                if attr.override:
                    attr.stat = attr.override
                    break
                else:
                    for mod_name, mod_val in attr.items():
                        if mod_name not in ['override', 'mod', 'stat',
                                            'disadv']:
                            try:
                                attr.stat += sum([mod_val])
                            except TypeError:
                                attr.stat += sum(mod_val)
                    attr.mod = int(mod_calc(attr.stat))

        def skills_and_saves():

            attrs = self.attributes

            skills = self.skills

            for skill in skills.values():
                skill['val'] = attrs[skill['attr']]['mod'] \
                               + self.stats.proficiency * skill['prof']
                for mod_name, mod_val in skill.items():
                    if not mod_name in ['val', 'name', 'attr', 'prof', 'notes',
                                        'disadv']:
                        skill['val'] += sum(mod_val)

            saves = self.saving_throws

            for save_name, save in saves.items():
                if save.override:
                    save.val = save.override
                else:
                    save.val = attrs[save_name].mod \
                               + self.stats.proficiency * save['prof']
                    for mod_name, mod_val in save.items():
                        if not mod_name in ['val', 'override', 'prof', 'notes']:
                            save.val += sum(mod_val)

        def HP():

            attrs = self.attributes
            classes = self.classes

            HP = 0

            for class_obj in classes.values():
                if class_obj.base_class:
                    HP += class_obj.hit_dice
                else:
                    HP += class_obj.lvl_up_hp

            HP += (self.info.level * attrs.CON.mod)
            self.stats.max_hp = int(HP)

        def senses():

            attrs = self.attributes
            senses = self.stats.senses

            senses.perception = 10 + attrs.WIS.mod
            senses.investigation = 10 + attrs.INT.mod
            senses.insight = 10 + attrs.WIS.mod

        def AC():

            stats = self.stats
            armoured = False

            AC = 0

            if not stats.armour_class.special:  ## special types to do later
                if self.worn.Body:
                    item = self.worn.Body[1]
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

            for item in self.wielded.keys():
                if item == 'Shield':
                    AC += 2

            for mod_name, mod_val in stats.armour_class.items():
                if not mod_name in ['value',
                                    'special']:  # recall overrides etc here
                    AC += sum(mod_val)

            if not armoured:
                AC += 10 + self.attributes['DEX']['mod']

            stats.armour_class['value'] = AC

        def proficiencies():

            for prof in self.proficiencies:
                prof_set = []
                prof_set = list(set(
                    [pro for pros in self.proficiencies[prof].values()
                     for pro in pros]))
                self.proficiencies[prof].set = prof_set

        def speed_and_size():

            self.stats.speed['value'] = 0
            self.stats.speed['value'] = sum(self.stats.speed.values())

            self.stats.size['current'] = self.stats.size.temp \
                                         or self.stats.size.race

        def attack_objects():

            self.actions.attacks = Dict()
            self.actions.attacks.update(
                {'Unarmed Strike': unarmed_strike(self)})
            for wielded, stats in self.wielded.items():
                if isclasstype(stats['obj'], 'Weapon'):
                    self.actions.attacks.update(
                        {wielded: atk_option(self, stats['obj'])})

        def penalties():

            no_longer = []

            if self.penalties:
                for item, penalties in self.penalties.items():

                    item_name = item.__class__.__name__.replace("_", " ")

                    worn_items = [item[0] for item in self.worn.values() if
                                  item]

                    if 'Armor STR' in penalties:
                        if item_name in worn_items \
                                and item.req > self.attributes.STR.stat:
                            self.stats.speed['Too weak for armour'] = -10
                        else:
                            del self.stats.speed['Too weak for armour']
                            self.penalties[item].remove('Armor STR')

                    if 'Armor Prof' in penalties:

                        cause = f'Armour proficiency: {item_name}'

                        if item_name in worn_items and \
                                item.armor_type not in self.proficiencies.armor.set:
                            self.attributes.STR['disadv'] += [cause]
                            self.attributes.DEX['disadv'] += [cause]
                            for skill_name, skill in self.skills.items():
                                if skill.attr in ['DEX', 'STR']:
                                    skill['disadv'] += [cause]

                            for atk, vals in self.actions.attacks.items():
                                vals.disadv += [cause]

                            self.other['can_cast_spells'] = False

                        else:
                            self.attributes.STR['disadv'].remove(cause)
                            self.attributes.DEX['disadv'].remove(cause)
                            for skill_name, skill in self.skills.items():
                                if skill.attr in ['DEX', 'STR']:
                                    skill['disadv'].remove(cause)

                                # for atk, vals in self.actions.attacks.items():
                                #     vals.disadv.remove(cause)

                            self.other['can_cast_spells'] = True
                            self.penalties[item].remove('Armor Prof')

                    if not penalties:
                        no_longer += [item]

            if no_longer:
                for item in no_longer:
                    del self.penalties[item]
                self.update()

        if not func:
            levels()
            modifiers()
            skills_and_saves()
            HP()
            senses()
            AC()
            proficiencies()
            speed_and_size()
            proficiencies()
            speed_and_size()
            attack_objects()
            penalties()

