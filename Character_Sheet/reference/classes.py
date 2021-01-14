from Character_Sheet.reference.items.weapons import *
from Character_Sheet.reference.items.armour import *
from Character_Sheet.reference.items.equipment import *
from Character_Sheet.reference.items.other import *
from Character_Sheet.reference.items.tools import *
from Character_Sheet.reference.skills_and_attributes import *


# Character descriptions from https://www.tribality.com/2019/01/08/brief-description-of-5e-classes-and-subclasses-ideal-to-show-to-your-players
# RPGbot hosts my personal favourite character guides, https://rpgbot.net/dnd5/characters/classes/.
# It focuses probably too heavily on character optimisation, so take it with a large pinch of salt.
# Remember that optimised builds are entirely valid, but ANY build is valid if it's fun.

class CharacterClass:
    pass


class Barbarian(CharacterClass):
    class_name = "Barbarian"

    desc = "Filled with their destructive rage and primal instincts, the Barbarian is the class you choose if you " \
           "want to be the meat shield in the front line dealing great amounts of damage. Who needs a shield when you " \
           "can stand your foes’ puny attacks with your hardened skin and/or high evasiveness? "

    rpgbot = "Barbarians are all about getting angry and dealing damage. They have a ton of hit points, resistance " \
             "to damage, and Rage gives a wonderful bonus to damage. Barbarians don't get much in the way of " \
             "skills, so generally they're stuck as combat monsters, but they function equally well as a Defender " \
             "and a Striker."

    primary_attr = STR,

    hit_die = 12
    lvl_up_hp = 7
    armour_proficiencies = Light, Medium, Shields
    weapon_proficiencies = Simple, Martial
    tool_proficiencies = None
    saving_throws = STR, CON
    num_skills = 2
    valid_skills = AnimalHandling, Athletics, Intimidation, Nature, Perception, Survival
    equipment = (
        ([(Greataxe, 1)],
         [((Martial, Melee), 1)]
         ),
        ([(Handaxe, 2)],
         [(Simple, 1)]
         ),
        ([(ExplorerPack, 1)]),
        ([(Javelin, 4)])
    )
    subclass_lvl = 3
    subclass_name = "Primal Path"


class Paladin(CharacterClass):
    class_name = "Paladin"
    desc = "A Paladin is a person guided by an oath, their force of will and devotion so strong they are granted the " \
           "ability to cast spells to smite their foes. They fight for justice and righteousness, with the idea of " \
           "following their oath and ideals to the very end. For this, they use heavy armor to be front liners and " \
           "protect their allies. "

    rpgbot = "Paladins are on the most durable, survivable, and self-sufficient class in the game. As such, " \
             "they make excellent solo characters. In a party, they serve as a Defender, Face, and Striker." \
             "\n\n" \
             "Paladins are extremely durable and can survive a long hard day of adventuring, but none of their " \
             "abilities (except Channel Divinity) recharge on a short rest, so you need to ration your resources more " \
             "strictly than many classes." \
             "\n\n" \
             "Paladins are also one of the more complex classes to play. They have a long list of class features, " \
             "touching on all of the games core mechanics. While this make them difficult for new players, this " \
             "also makes the Paladin a great introductory class because the player needs to learn so much to play " \
             "it. "

    primary_attr = STR, CHA

    hit_die = 10
    lvl_up_hp = 6
    armour_proficiencies = Light, Medium, Heavy, Shields
    weapon_proficiencies = Simple, Martial
    tool_proficiencies = None
    saving_throws = WIS, CHA
    num_skills = 2
    valid_skills = Athletics, Insight, Intimidation, Medicine, Persuasion, Religion
    subclass_lvl = 3
    equipment = (
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
    subclass_name = "Sacred Oath"


class Rogue(CharacterClass):
    class_name = "Rogue"

    desc = "Let’s get shady, grab a dagger and start stabbing. Rogues excel at sneaking around, scouting ahead, " \
           "being dexterous and about everything you would expect a thief to be good at. In dungeons, they can help " \
           "their party by deactivating traps or opening locked doors. Don’t expect them to wear much armor, " \
           "nor be able to carry heavy stuff; but if your task should need some delicacy or swashbuckling, " \
           "you’ve found the right person. "

    rpgbot = "Rogues are the quintessential Face, Scout and Striker. Sneak Attack allows them to do a huge pile of " \
             "damage in a single attack, and their pile of skills allows them to easily handle locks, traps, guards, " \
             "and many other challenges. While a party can function just fine without a Rogue, it's hard to compete " \
             "with the sheer number of important skill and tool proficiencies offered by the Rogue." \
             "\n\n" \
             "Rogues split into melee or ranged builds. Melee Rogues frequently go for two-weapon fighting because " \
             "it provides a second chance to score Sneak Attack, and hit-and-run tactics are great way to get into " \
             "melee to attack before retreating behind your party. Ranged rogues (archer Rogues) typically rely on " \
             "sniping. Hiding after each attack using Cunning Action is reliable and effective, though it can be " \
             "very static and repetitive. Arcane Tricksters expand on these options with magic, but when it's time " \
             "to kill stuff even tricksters use the same tactics. "

    primary_attr = DEX,

    hit_die = 8
    lvl_up_hp = 5
    armour_proficiencies = Light,
    weapon_proficiencies = Simple, HandCrossbow, Longsword, Rapier, Shortsword
    tool_proficiencies = ThievesTools,
    saving_throws = DEX, INT
    num_skills = 4
    valid_skills = Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, \
                   Persuasion, SleightOfHand, Stealth
    equipment = (
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
    subclass_lvl = 3
    subclass_name = "Roguish Archetype"


class Wizard(CharacterClass):
    class_name = "Wizard"

    desc = "Wizards decide to go in adventures to further their knowledge. The great world in front of them has " \
           "thousands of spells for you to learn and master. With a spellbook at hand, they will look for or buy them " \
           "to become a greater spellcaster. Just transcribe them to the book and you’ll understand why Wizards are " \
           "such a versatile class. The amount of spells they can learn greatly surpasses all other classes’ lists. "

    rpgbot = "The Wizard is the iconic arcane spellcaster, capable of doing all manner of fantastic tricks, " \
             "and generally limited only by their spellbook. A Wizard with a comprehensive spellbook can do " \
             "essentially anything in the game, often as well as or better than a non-magical character who is built " \
             "to do that thing. A Wizard with Invisibility is as stealthy as a Rogue. A Wizard with a summoned pet " \
             "can replace a fighter (at least temporarily). A clever Wizard could even find a way to heal his allies " \
             "and replace a Cleric.\n\nBecause Wizards can do so much so well, their roles are numerous and varied. " \
             "However, in a typical party the Wizard's primary functions are as a Blaster, Striker, and Utility " \
             "Caster. "

    primary_attr = INT,

    hit_die = 6
    lvl_up_hp = 4
    armour_proficiencies = None
    weapon_proficiencies = Dagger, Dart, Sling, Quarterstaff, LightCrossbow
    tool_proficiencies = None
    saving_throws = INT, WIS
    num_skills = 2
    valid_skills = Arcana, History, Insight, Investigation, Medicine, Religion
    equipment = (
        ([(Quarterstaff, 1)],
         [(Dagger, 1)]
         ),
        ([(ComponentPouch, 1)],
         [(ArcaneFocus, 1)]
         ),
        ([(ScholarPack, 1)],
         [(ExplorerPack, 1)]
         ),
        ([(Spellbook, 1)])
    )
    subclass_lvl = 2
    subclass_name = "Arcane Tradition"


class_list = {class_.class_name: class_ for class_ in CharacterClass.__subclasses__()}

if __name__ == '__main__':
    pass
