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
