class Darkvision:
    def __init__(self, race, distance):
        self.race = race
        self.distance = distance
        self.desc = f'Thanks to your {self.race} blood, you have superior vision in dark and dim Conditions. You can ' \
                    f'see in dim light within {self.distance} feet of you as if it were bright light, and in Darkness ' \
                    f'as if it were dim light. You can’t discern color in Darkness, only Shades of Gray. '


class Menacing:
    def __init__(self):
        self.desc = f'You gain proficiency in the Intimidation skill.'


class RelentlessEndurance:
    def __init__(self):
        self.desc = f"When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point " \
                    f"instead. You can't use this feature again until you have finished a long rest. "


class SavageAttacks:
    def __init__(self):
        self.desc = f"When you score a critical hit with a melee weapon attack, you can roll one of the weapon's " \
                    f"damage dice one additional time and add it to the extra damage of the critical hit. "


class FeyAncestry:
    def __init__(self):
        self.desc = f"You have advantage on saving throws against being charmed, and magic can't put you to sleep."


class KeenSenses:
    def __init__(self):
        self.desc = f"You have proficiency in the perception skill. [Why would you choose this?]"


class ElfWeaponTraining:
    def __init__(self):
        self.desc = f"You have proficiency with the longsword, shortsword, shortbow, and longbow."


class FleetOfFoot:
    def __init__(self):
        self.desc = f"Your base walking speed increases to 35 feet."


class MaskOfTheWild:
    def __init__(self):
        self.desc = f"You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, " \
                    f"falling snow, mist, or other natural phenomena. "


class Catrip:
    def __init__(self, num="one", spell_list="", spellcasting_ability=""):
        if spell_list:
            spell_list = f" from the {spell_list} spell list"

        if spellcasting_ability:
            spellcasting_ability = f' {spellcasting_ability.capitalize()} is your spellcasting ability for it.'

        self.desc = f"You know {num} cantrip of your choice{spell_list}.{spellcasting_ability}"


class DrowMagic:
    def __init__(self):
        self.desc = f"You know the Dancing Lights cantrip.\nWhen you reach 3rd level, you can cast the faerie fire " \
                    f"spell once per day; you must finish a long rest in order to cast the spell again using this " \
                    f"trait.\nWhen you reach 5th level, you can also cast hte darkness spell once per day; you must " \
                    f"finish a long rest in order to cast the spell again using this trait. Charisma is you " \
                    f"spellcasting ability for these spells. "  # TODO: May be able to automate this.


class Swim:
    def __init__(self):
        self.desc = f"You gain a swimming speed of 30 feet."


class PowerfulBuild:
    def __init__(self):
        self.desc = f"You count as one size larger when determining your carrying capacity and the weight you can " \
                    f"push, drag, or lift. "


class LoxodonSerenity:
    def __init__(self):
        self.desc = f"You have advantage against being charmed or frightened."


class NaturalArmour:
    def __init__(self):
        self.desc = f"You have thick, leathery skin. When you aren't wearing armor, your AC is 12 + your Constitution " \
                    f"modifier. You can use your natural armor to determine your AC if the armor you wear would leave " \
                    f"you with a lower AC. A shield's benefits apply as normal while you use your natural armor. "


class Trunk:
    def __init__(self):
        self.desc = f"You can grasp things with your trunk, and you can use it as a snorkel. It has a reach of 5 " \
                    f"feet, and it can lift a number of pounds equal to five times your Strength score. You can use " \
                    f"it to do the following simple tasks: lift, drop, hold, push, or pull an object or a creature; " \
                    f"open or close a door or a container; grapple someone; or make an unarmed strike. Your DM might " \
                    f"allow other simple tasks to be added to that list of options. It can't wield weapons or shields " \
                    f"or do anything that requires manual precision, such as using tools or magic items or performing " \
                    f"the somatic components of a spell. "


class KeenSmell:
    def __init__(self):
        self.desc = f"Thanks to your sensitive trunk, you have advantage on Wisdom (Perception), Wisdom (Survival), " \
                    f"and Intelligence (Investigation) checks that involve smell."


class ConstructedResilience:
    def __init__(self):
        self.desc = f"You were created to have remarkable fortitude, represented by the following benefits:" \
                    f"\n \u2022 You have advantage on saving throws against being poisoned, and you have resistance to poison " \
                    f"damage." \
                    f"\n \u2022 You don’t need to eat, drink, or breathe." \
                    f"\n \u2022 You are immune to disease." \
                    f"\n \u2022 You don't need to sleep, and magic can't put you to sleep."


class SentrysRest:
    def __init__(self):
        self.desc = f"When you take a long rest, you must spend at least six hours in an inactive, motionless state, " \
                    f"rather than sleeping. In this state, you appear inert, but it doesn’t render you unconscious, " \
                    f"and you can see and hear as normal. "


class IntegratedProtection:
    def __init__(self):
        self.desc = f"Your body has built-in defensive layers, which can be enhanced with armor." \
                    f"\n \u2022 You gain a +1 bonus to Armor Class." \
                    f"\n \u2022 You can don only armor with which you have proficiency. To don armor, you must incorporate it " \
                    f"into your body over the course of 1 hour, during which you must remain in contact with the " \
                    f"armor. To doff armor, you must spend 1 hour removing it. You can rest while donning or doffing " \
                    f"armor in this way." \
                    f"\n \u2022 While you live, your armor can't be removed from your body against your will."
