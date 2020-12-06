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


# Weapons

class Javelin(Simple, Melee):
    pass


class Longsword(Martial, Melee):
    pass


class Rapier(Martial, Melee):
    pass


class Shortsword(Martial, Melee):
    pass


class HandCrossbow(Martial, Ranged):
    pass


# Armour

class ChainMail(Heavy):
    pass


# Misc.

class HolySymbol(Misc):
    pass


# Packs

class PriestPack(Pack):
    pass


class ExplorerPack(Pack):
    pass


if __name__ == '__main__':
    pass
