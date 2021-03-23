import Character_Sheet.reference.skills_and_attributes as skills
import Character_Sheet.reference.items as items
import Character_Sheet.reference.glossary as glossary

class FeatureTypes:

    def text_feature(self, vals):
        self.char.Features["Other"][self.name] = vals

    class Prof:
        def skills(self, skills_list):
            for skill in skills_list:
                self.char.skills[skill.name].prof = True

        def armours(self, armours):
            for armour in armours:
                self.char.proficiencies["Armour"][armour.name] = True

        def weapons(self, weapons):
            for weapon in weapons:
                self.char.proficiencies["Weapons"][weapon.name] = True

        def tools(self, tools):
            for tool in tools:
                self.char.proficiencies["Tools"][tool.name] = True

    def defence(self, vals):
        self.char.Defences += vals

    def immunity(self, vals):
        self.char.immunities += vals

    def saves(self, vals):
        print("saves features not added yet.")

    def save_notes(self, vals):
        for val in vals:
            attr = val[0]
            note = val[1]
            if attr:
                self.char.saving_throws[attr].notes += note
            else:
                self.char.saving_throws["Notes"] += note

    def speed(self, speed):
        self.info["speed"].override["base"] =+ [speed]

    def cantrips(self, vals):
        keys = vals.keys()
        if "cantrips" in keys:
            print("Specific Cantrips")
            print(vals["cantrips"])
        elif "num" in keys and "spell_list" in keys:
            print("Choosing cantrips")

    def swim(self, vals):
        if "swim speed" in self.info:
            self.info["swim_speed"] += [vals]
        else:
            self.info["swim_speed"] = [vals],

class Feature:

    def add(self, char, name):
        print("Adding feature, implementation incomplete!")
        # self.name = name
        # self.char = char
        #
        # self.char.Features["All"][name] = self.desc
        #
        # if hasattr(self, "effects"):
        #
        #     if not isinstance(self.effects[0], tuple):
        #         self.effects = (self.effects),
        #
        #     for feature_effect in self.effects:
        #         func, vals = feature_effect
        #         func(self, vals)
        # else:
        #     FeatureTypes.text_feature(self, self.desc)
        #     print(F"{self.name} implementation incomplete.")


class Darkvision(Feature):
    def __init__(self, race, distance):
        self.desc = f'Thanks to your {race} blood, you have superior vision in dark and dim Conditions. You can ' \
                    f'see in dim light within {distance} feet of you as if it were bright light, and in Darkness ' \
                    f'as if it were dim light. You can’t discern color in Darkness, only Shades of Gray. '

        self.effects = (FeatureTypes.text_feature, [self.desc]),


class Darkvision2(Feature):
    def __init__(self, reason, distance):
        self.desc = f'{reason}, you have superior vision in dark and dim Conditions. You can ' \
                    f'see in dim light within {distance} feet of you as if it were bright light, and in Darkness ' \
                    f'as if it were dim light. You can’t discern color in Darkness, only Shades of Gray. '

        self.effects = (FeatureTypes.text_feature, [self.desc]),


class SuperiorDarvision(Feature):
    def __init__(self, distance):
        self.desc = f"You can see in dim light within {distance} feet of you as if it were bright light, and in " \
                    f"darkness as if it were dim light. You can't discern color in darkness, only Shades of Gray. "

        self.effects = (FeatureTypes.text_feature, [self.desc]),


class Menacing(Feature):
    def __init__(self):
        self.desc = f'You gain proficiency in the Intimidation skill.'

        self.effects = (FeatureTypes.Prof.skills, [skills.Intimidation]),


class RelentlessEndurance(Feature):
    def __init__(self):
        self.desc = f"When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point " \
                    f"instead. You can't use this feature again until you have finished a long rest. "

        self.effects = (FeatureTypes.text_feature, [self.desc]),  # Improve


class SavageAttacks(Feature):
    def __init__(self):
        self.desc = f"When you score a critical hit with a melee weapon attack, you can roll one of the weapon's " \
                    f"damage dice one additional time and add it to the extra damage of the critical hit. "

        self.effects = (FeatureTypes.text_feature, [self.desc]),  # Improve


class FeyAncestry(Feature):
    def __init__(self):
        self.desc = f"You have advantage on saving throws against being charmed, and magic can't put you to sleep."

        self.effects = (FeatureTypes.defence, ["Magic can't put you to sleep"]), \
                       (FeatureTypes.save_notes, [(None, "Advantage on saves against being charmed"),])


class KeenSenses(Feature):
    def __init__(self):
        self.desc = f"You have proficiency in the perception skill. [Why would you choose this?]"

        self.effects = (FeatureTypes.Prof.skills, [skills.Perception]),


class ElfWeaponTraining(Feature):
    def __init__(self):
        self.desc = f"You have proficiency with the longsword, shortsword, shortbow, and longbow."

        self.effects = (FeatureTypes.Prof.weapons, [items.Longsword, items.Shortsword, items.Longbow]),


class FleetOfFoot(Feature):
    def __init__(self):
        self.desc = f"Your base walking speed increases to 35 feet."

        self.effects = (FeatureTypes.speed, 35),


class MaskOfTheWild(Feature):
    def __init__(self):
        self.desc = f"You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, " \
                    f"falling snow, mist, or other natural phenomena. "

        self.effects = (FeatureTypes.text_feature, [self.desc]),


class Catrip(Feature):
    def __init__(self, num="one", spell_list="", spellcasting_ability=""):
        if spell_list:
            spell_list = f" from the {spell_list} spell list"

        if spellcasting_ability:
            spellcasting_ability = f' {spellcasting_ability.capitalize()} is your spellcasting ability for it.'

        self.desc = f"You know {num} cantrip of your choice{spell_list}.{spellcasting_ability}"

        self.effects = (FeatureTypes.cantrips, dict(num=num, spell_list=spell_list, ability=spellcasting_ability)),


class DrowMagic(Feature):
    def __init__(self):
        self.desc = f"You know the Dancing Lights cantrip.\nWhen you reach 3rd level, you can cast the faerie fire " \
                    f"spell once per day; you must finish a long rest in order to cast the spell again using this " \
                    f"trait.\nWhen you reach 5th level, you can also cast the darkness spell once per day; you must " \
                    f"finish a long rest in order to cast the spell again using this trait. Charisma is you " \
                    f"spellcasting ability for these spells. "  # TODO: May be able to automate this.

        cantrips_list = (1, "Dancing Lights"), \
                        (3, "Faerie Fire"), \
                        (5, "Darkness")

        self.effects = (FeatureTypes.cantrips, dict(cantrips=cantrips_list, ability=skills.CHA, recharge=glossary.long_rest))

class Swim(Feature):
    def __init__(self):
        self.desc = f"You gain a swimming speed of 30 feet."

        self.effects = (FeatureTypes.swim, 30)


class PowerfulBuild(Feature):
    def __init__(self):
        self.desc = f"You count as one size larger when determining your carrying capacity and the weight you can " \
                    f"push, drag, or lift. "

        self.effects = (FeatureTypes.text_feature, [self.desc]),


class LoxodonSerenity(Feature):
    def __init__(self):
        self.desc = f"You have advantage against being charmed or frightened."

        self.effects = (FeatureTypes.save_notes, [(None, "Advantage against being charmed or frightened."),])

class NaturalArmour(Feature):
    def __init__(self):
        self.desc = f"You have thick, leathery skin. When you aren't wearing armor, your AC is 12 + your Constitution " \
                    f"modifier. You can use your natural armor to determine your AC if the armor you wear would leave " \
                    f"you with a lower AC. A shield's benefits apply as normal while you use your natural armor. "


class Trunk(Feature):
    def __init__(self):
        self.desc = f"You can grasp things with your trunk, and you can use it as a snorkel. It has a reach of 5 " \
                    f"feet, and it can lift a number of pounds equal to five times your Strength score. You can use " \
                    f"it to do the following simple tasks: lift, drop, hold, push, or pull an object or a creature; " \
                    f"open or close a door or a container; grapple someone; or make an unarmed strike. Your DM might " \
                    f"allow other simple tasks to be added to that list of options. It can't wield weapons or shields " \
                    f"or do anything that requires manual precision, such as using tools or magic items or performing " \
                    f"the somatic components of a spell. "


class KeenSmell(Feature):
    def __init__(self):
        self.desc = f"Thanks to your sensitive trunk, you have advantage on Wisdom (Perception), Wisdom (Survival), " \
                    f"and Intelligence (Investigation) checks that involve smell."


class ConstructedResilience(Feature):
    def __init__(self):
        self.desc = f"You were created to have remarkable fortitude, represented by the following benefits:" \
                    f"\n \u2022 You have advantage on saving throws against being poisoned, and you have resistance to poison " \
                    f"damage." \
                    f"\n \u2022 You don’t need to eat, drink, or breathe." \
                    f"\n \u2022 You are immune to disease." \
                    f"\n \u2022 You don't need to sleep, and magic can't put you to sleep."


class SentrysRest(Feature):
    def __init__(self):
        self.desc = f"When you take a long rest, you must spend at least six hours in an inactive, motionless state, " \
                    f"rather than sleeping. In this state, you appear inert, but it doesn’t render you unconscious, " \
                    f"and you can see and hear as normal. "


class IntegratedProtection(Feature):
    def __init__(self):
        self.desc = f"Your body has built-in defensive layers, which can be enhanced with armor." \
                    f"\n \u2022 You gain a +1 bonus to Armor Class." \
                    f"\n \u2022 You can don only armor with which you have proficiency. To don armor, you must incorporate it " \
                    f"into your body over the course of 1 hour, during which you must remain in contact with the " \
                    f"armor. To doff armor, you must spend 1 hour removing it. You can rest while donning or doffing " \
                    f"armor in this way." \
                    f"\n \u2022 While you live, your armor can't be removed from your body against your will."


class DwarvenStoutness(Feature):
    def __init__(self):
        self.desc = f"Your speed is not reduced by wearing heavy armour."


class DwarvenResilience(Feature):
    def __init__(self):
        self.desc = f"You have advantage on saving throws against poison, and you have resistance against poison damage."


class DwarvenCombatTraining(Feature):
    def __init__(self):
        self.desc = f"You have proficiency with the battleaxe, handaxe, light hammer, and warhammer."


class Stonecunning(Feature):
    def __init__(self):
        self.desc = f"Whenever you make an Intelligence (History) check related to the origin of stonework, " \
                    f"you are considered proficient in the History skill and add double your proficiency bonus to the " \
                    f"check, instead of your normal proficiency bonus. "


class DwarvenToughness(Feature):
    def __init__(self):
        self.desc = f"Your hit point maximum increases by 1, and it increases by 1 every time you gain a level."


class DwarvenArmourTraining(Feature):
    def __init__(self):
        self.desc = f"You have proficiency with light and medium armour."


class DuergarResilience(Feature):
    def __init__(self):
        self.desc = f"You have advantage on saving throws against illusions and against being charmed or paralyzed."


class DuergarMagic(Feature):
    def __init__(self):
        self.desc = f"When you reach 3rd level, you can cast the Enlarge/Reduce spell on yourself once with this " \
                    f"trait, using only the spell's enlarge option. When you reach 5th level, you can cast the " \
                    f"Invisibility spell on yourself once with this trait. You don't need material components for " \
                    f"either spell, and you can't cast them while you're in direct sunlight, although sunlight has no " \
                    f"effect on them once cast. You regain the ability to cast these spells with this trait when you " \
                    f"finish a long rest. Intelligence is your spellcasting ability for these spells. "


class SunlightSensitivity(Feature):
    def __init__(self):
        self.desc = f"You have disadvantage on Attack rolls and Wisdom (Perception) checks that rely on sight when " \
                    f"you, the target of your attack, or whatever you are trying to perceive is in direct sunlight. "
