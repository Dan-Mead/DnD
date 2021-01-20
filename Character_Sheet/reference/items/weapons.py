from Character_Sheet.reference.items.items_key import Item, Weapon
from Character_Sheet.reference.items.jargon import *


Props = Weapon.PropertyKeys

class Simple(Weapon):
    name = "Simple"
    suffix = "Weapon"
    plural = 0

class Martial(Weapon):
    name = "Martial"
    suffix = "Weapon"
    plural = 0

class Improvised(Weapon):
    name = "Improvised"
    suffix = "Weapon"
    plural = 0

class Ranged(Weapon):
    name = "Ranged"
    suffix = "Weapon"
    plural = 0

class Melee(Weapon):
    name = "Melee"
    suffix = "Weapon"
    plural = 0


class Club(Simple, Melee):
    name = "Club"
    plural = 0
    cost = sp(1)
    dmg = (1, 4, b)
    weight = 2
    properties = Weapon.properties(Props.light)

class Dagger(Simple, Melee):
    name = "Dagger"
    plural = 0
    cost = (2, gp)
    dmg = (1, 4, s)
    weight = 1
    properties = Weapon.properties(Props.finesse, Props.light, Props.thrown(20, 60))


class Greatclub(Simple, Melee):
    name = "Greatclub"
    plural = 0
    cost = (2, gp)
    dmg = (1, 8, b)
    weight = 10
    properties = Weapon.properties(Props.two_handed)


class Handaxe(Simple, Melee):
    name = "Handaxe"
    plural = 0
    cost = (5, gp)
    dmg = (1, 6, s)
    weight = 2
    properties = Weapon.properties(Props.light, Props.thrown(20, 60))


class Javelin(Simple, Melee):
    name = "Javelin"
    plural = 0


class LightHammer(Simple, Melee):
    name = "Light Hammer"
    plural = 0


class Mace(Simple, Melee):
    name = "Mace"
    plural = 0


class Quarterstaff(Simple, Melee):
    name = "Quarterstaff"
    plural = 0


class Sickle(Simple, Melee):
    name = "Sickle"
    plural = 0


class Spear(Simple, Melee):
    name = "Spear"
    plural = 0


class LightCrossbow(Simple, Ranged):
    name = "Light Crossbow"
    plural = 0


class Dart(Simple, Ranged):
    name = "Dart"
    plural = 0


class Shortbow(Simple, Ranged):
    name = "Shortbow"
    plural = 0


class Sling(Simple, Ranged):
    name = "Sling"
    plural = 0


class Battleaxe(Martial, Melee):
    name = "Battleaxe"
    plural = 0


class Flail(Martial, Melee):
    name = "Flail"
    plural = 0


class Glaive(Martial, Melee):
    name = "Glaive"
    plural = 0


class Greataxe(Martial, Melee):
    name = "Greataxe"
    plural = 0


class Greatsword(Martial, Melee):
    name = "Greatsword"
    plural = 0


class Halberd(Martial, Melee):
    name = "Halberd"
    plural = 0


class Lance(Martial, Melee):
    name = "Lance"
    plural = 0


class Longsword(Martial, Melee):
    name = "Longsword"
    plural = 0


class Maul(Martial, Melee):
    name = "Maul"
    plural = 0


class Morningstar(Martial, Melee):
    name = "Morningstar"
    plural = 0


class Pike(Martial, Melee):
    name = "Pike"
    plural = 0


class Rapier(Martial, Melee):
    name = "Rapier"
    plural = 0


class Shortsword(Martial, Melee):
    name = "Shortsword"
    plural = 0


class Scimitar(Martial, Melee):
    name = "Scimitar"
    plural = 0


class Shortsword(Martial, Melee):
    name = "Shortsword"
    plural = 0


class Trident(Martial, Melee):
    name = "Trident"
    plural = 0


class WarPick(Martial, Melee):
    name = "War Pick"
    plural = 0


class Warhammer(Martial, Melee):
    name = "Warhammer"
    plural = 0


class Whip(Martial, Melee):
    name = "Whip"
    plural = 0


class Blowgun(Martial, Ranged):
    name = "Blowgun"
    plural = 0


class HandCrossbow(Martial, Ranged):
    name = "Hand Crossbow"
    plural = 0


class HeavyCrossbow(Martial, Ranged):
    name = "Heavy Crossbow"
    plural = 0


class Longbow(Martial, Ranged):
    name = "Longbow"
    plural = 0

from dataclasses import dataclass


class Net(Martial, Ranged):
    name = "Net"
    plural = 0
    cost = 1, gp
    weight = 3