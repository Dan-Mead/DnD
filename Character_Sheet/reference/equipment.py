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

class Club(Simple, Melee):
    name = "Club"


class Dagger(Simple, Melee):
    name = "Dagger"


class Greatclub(Simple, Melee):
    name = "Greatclub"


class Handaxe(Simple, Melee):
    name = "Handaxe"


class Javelin(Simple, Melee):
    name = "Javelin"


class LightHammer(Simple, Melee):
    name = "Light Hammer"


class Mace(Simple, Melee):
    name = "Mace"


class Quarterstaff(Simple, Melee):
    name = "Quarterstaff"


class Sickle(Simple, Melee):
    name = "Sickle"


class Spear(Simple, Melee):
    name = "Spear"


class LightCrossbow(Simple, Ranged):
    name = "Light Crossbow"


class Dart(Simple, Ranged):
    name = "Dart"


class Shortbow(Simple, Ranged):
    name = "Shortbow"


class Sling(Simple, Ranged):
    name = "Sling"


class Battleaxe(Martial, Melee):
    name = "Battleaxe"


class Flail(Martial, Melee):
    name = "Flail"


class Glaive(Martial, Melee):
    name = "Glaive"


class Greataxe(Martial, Melee):
    name = "Greataxe"


class Greatsword(Martial, Melee):
    name = "Greatsword"


class Halberd(Martial, Melee):
    name = "Halberd"


class Lance(Martial, Melee):
    name = "Lance"


class Longsword(Martial, Melee):
    name = "Longsword"


class Maul(Martial, Melee):
    name = "Maul"


class Morningstar(Martial, Melee):
    name = "Morningstar"


class Pike(Martial, Melee):
    name = "Pike"


class Rapier(Martial, Melee):
    name = "Rapier"


class Shortsword(Martial, Melee):
    name = "Shortsword"


class Scimitar(Martial, Melee):
    name = "Scimitar"


class Shortsword(Martial, Melee):
    name = "Shortsword"


class Trident(Martial, Melee):
    name = "Trident"


class WarPick(Martial, Melee):
    name = "War Pick"


class Warhammer(Martial, Melee):
    name = "Warhammer"


class Whip(Martial, Melee):
    name = "Whip"


class Blowgun(Martial, Ranged):
    name = "Blowgun"


class HandCrossbow(Martial, Ranged):
    name = "Hand Crossbow"


class HeavyCrossbow(Martial, Ranged):
    name = "Heavy Crossbow"


class Longbow(Martial, Ranged):
    name = "Longbow"


class Net(Martial, Ranged):
    name = "Net"


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
