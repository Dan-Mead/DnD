# DnD

Repo for DnD work, mainly just cls stuff at the moment.
Slightly abused PEP 8 stylistic on a lot of Class names but just seemed to
 make it a lot more readable.

#Taxonomy

This is a general guide to the structure of this work, as well as a brief
 description of how each section behaves and is constructed.

## Aspects

Aspects is concerned with cls creation, and building a 'cls
' object. The cls object contains all the information required for the
 cls sheet to build an object. And will [TBD] be exportable.
 
 Stats currently included are:
 
 * Info - Character description and qualitative stats. Generally immutable
  information.
 * Bio - Flavour and backstory. Designed entirely for roleplaying.
 * Stats - Values that actively affect the game, HP, defences etc.
 * Attributes - Classic DnD attributes, values, modifiers, and temp values.
 * Skills - Skills as well as profficiencies and notes.
 * Saving Throws - modifiers and notes.
 * Profficiencies - Tools, weapons, armor, and languages.
 * Items - Currency, attire, and equipment.  
 * Feats - Feats and their effects.
 * Features - Features from various other aspects and their effects.
 * Actions [TBD]
    * Free Actions - Usable at any time.
    * Attacks
    * Bonus
    * Reaction
 
 * Backgrounds [TBD]
 * Spells [TBD]
    * Action type?


Note: There is an overlap / redundancy with how effects work. Some features
 such as Races effectively add effects but as they were coded first and work
  slightly differently then they are added as a different mechanic.

