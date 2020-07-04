attrs = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

common_languages = ["Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc"]
exotic_languages = ["Abyssal", "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan",
                    "Undercommon"]

ordinals = ["First", "Second", "Third", "Next"]

skills_dict = dict(acrobatics=["Acrobatics", "DEX"], animal_handling=["Animal Handling", "WIS"],
                   arcana=["Arcana", "INT"], athletics=["Athletics", "STR"], deception=["Deception", "CHA"],
                   history=["History", "INT"], insight=["Insight", "WIS"], intimidation=["Intimidation", "CHA"],
                   investigation=["Investigation", "INT"], medicine=["Medicine", "WIS"], nature=["Nature", "INT"],
                   perception=["Perception", "WIS"], performance=["Performance", "CHA"],
                   persuasion=["Persuasion", "CHA"], religion=["Religion", "INT"],
                   sleight_of_hand=["Sleight of Hand", "DEX"], stealth=["Stealth", "DEX"], survival=["Survival", "WIS"])

weapon_properties = {
    'Ammunition': 'You can use a weapon that has the Ammunition property to make a ranged Attack only if you have '
                  'Ammunition to fire from the weapon. Each time you Attack with the weapon, you expend one piece '
                  'of Ammunition. Drawing the Ammunition from a Quiver, case, or other container is part of the '
                  'Attack (you need a free hand to load a one-handed weapon). At the end of the battle, '
                  'you can recover half your expended Ammunition by taking a minute to Search the battlefield. If '
                  'you use a weapon that has the Ammunition property to make a melee Attack, you treat the weapon '
                  'as an Improvised Weapon (see “Improvised Weapons” later in the section). A sling must be loaded to '
                  'deal any damage when used in this way.',

    'Finesse': 'When Making an Attack with a finesse weapon, you use your choice of your Strength or Dexterity '
               'modifier for the Attack and Damage Rolls. You must use the same modifier for both rolls.',

    'Heavy': 'Small creatures have disadvantage on Attack rolls with heavy Weapons. A heavy weapon’s size and bulk '
             'make it too large for a Small creature to use effectively.',

    'Light': 'A light weapon is small and easy to handle, making it ideal for use when fighting with two Weapons.',

    'Loading': 'Because of the time required to load this weapon, you can fire only one piece of Ammunition from it '
               'when you use an action, Bonus Action, or Reaction to fire it, regardless of the number of attacks you '
               'can normally make.',

    'Range': 'A weapon that can be used to make a ranged Attack has a range in parentheses after the Ammunition or '
             'thrown property. The range lists two numbers. The first is the weapon’s normal range in feet, '
             'and the second indicates the weapon’s long range. When attacking a target beyond normal range, '
             'you have disadvantage on the Attack roll. You can’t Attack a target beyond the weapon’s long range.',

    'Reach': 'This weapon adds 5 feet to your reach when you Attack with it, as well as when determining your reach '
             'for Opportunity Attacks with it.',

    'Special': {
        'Lance': 'You have disadvantage when you use a lance to Attack a target within 5 feet of you. Also, '
                 'a lance requires two hands to wield when you aren’t mounted.',
        'Net': 'A Large or smaller creature hit by a net is Restrained until it is freed. A net has no effect on '
               'creatures that are formless, or creatures that are Huge or larger. A creature can use its action to '
               'make a DC 10 Strength check, freeing itself or another creature within its reach on a success. '
               'Dealing 5 slashing damage to the net (AC 10) also frees the creature without harming it, ending the '
               'effect and destroying the net. When you use an action, Bonus Action, or Reaction to Attack with a '
               'net, you can make only one Attack regardless of the number of attacks you can normally make.'},

    'Thrown': 'If a weapon has the thrown property, you can throw the weapon to make a ranged Attack. If the weapon '
              'is a melee weapon, you use the same ability modifier for that Attack roll and damage roll that you '
              'would use for a melee Attack with the weapon. For example, if you throw a Handaxe, you use your '
              'Strength, but if you throw a Dagger, you can use either your Strength or your Dexterity, '
              'since the Dagger has the finesse property.',

    'Two-handed': 'This weapon requires two hands when you Attack with it.',

    'Versatile': 'This weapon can be used with one or two hands. A damage value in parentheses appears with the '
                 'property—the damage when the weapon is used with two hands to make a melee Attack.',

    'Silvered': 'Some Monsters that have immunity or Resistance to nonmagical Weapons are susceptible to silver '
                'Weapons, so cautious adventurers invest extra coin to plate their Weapons with silver. You can '
                'silver a single weapon or ten pieces of Ammunition for 100 gp. This cost represents not only the '
                'price of the silver, but the time and expertise needed to add silver to the weapon without making it '
                'less effective. '
}
