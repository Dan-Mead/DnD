import inspect
import sys
from Character_Sheet.reference.glossary import attrs
from Character_Sheet.reference.features import *
from Character_Sheet.reference.proficiencies import *


# Types

class Ranged(Weapon):
    pass


class Melee(Weapon):
    pass


class Pack(Equipment):
    pass


class Misc(Equipment):
    pass


class Ammo(Equipment):
    pass

class Tools(Equipment):
    pass

# Weapons

class Dagger(Simple, Melee):
    name = "Dagger"

class Javelin(Simple, Melee):
    name = "Javelin"


class Shortbow(Simple, Ranged):
    name = "Shortbow"


class Longsword(Martial, Melee):
    name = "Longsword"


class Rapier(Martial, Melee):
    name = "Rapier"


class Shortsword(Martial, Melee):
    name = "Shortsword"


class HandCrossbow(Martial, Ranged):
    name = "Hand Crossbow"


# Other

class Arrow(Ammo):
    name = "Arrow"


# Armour

class LeatherArmour(Light):
    name = "Leather Armour"

class ChainMail(Heavy):
    name = "Chain Mail"

class Shield(Shields):
    name = "Shield"

# Misc.

class HolySymbol(Misc):
    name = "Holy Symbol"


# Packs

class PriestPack(Pack):
    name = "Priest's Pack"


class ExplorerPack(Pack):
    name = "Explorer's Pack"

class BurglarPack(Pack):
    name = "Burglar's Pack"

class DungeoneerPack(Pack):
    name = "Dungeoneer's Pack"


# Tools

class ThievesTools(Tools):
    name = "Thieves' Tools"

if __name__ == '__main__':
    pass
