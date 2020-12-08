# DnD

Repo for my personal DnD project work. End goal is an automated character sheet, similar to Dnd Beyond but without paywalls for content (means I cannot distribute this subsequently). Written entirely in Python, using Tkinter for GUI components.

Currently, the character creator GUI is working. Using it you can create a character, give it basic information, assign one of the implemented races and classes. Saving and loading should fully work. Some class features are incomplete.

Next stages are:
* Finish off class features (equipment, subclass selection if appropriate)
* Add prerequisites for feats
* Add backstories (including custom backstories)
* Eventually, import all to the master character sheet.

Current working features:

## Character Creator

### Basic character information
* Name
* Physical Information
* Alignment / Morality
### Races    
* Races included:
    * Half-Orc
    * Half-Elf
        * All variants
    * Human
        * All variants
* Race and subrace selection
* Race languages
* Race size and speed
* Race ASIs (including choices)
* Race skills (where relevant)
* Other race features
    
### Classes
* Classes currently included:
    * Paladin
    * Rogue
    * Barbarian
* Class selection (subclasses [TBD])
* Class Proficiencies
* Class skill selection
* Class equipment [WIP]

### Backgrounds [TBD]

### Other

* Equipment
    * All Weapons listed, not fully detailed
    * Some armours done
    * Some misc. items, packs etc. done
* Proficiencies
    * Most generated
    
* Feats
    * Some started, prerequisites [TBD] until classes and background fully implemented.
