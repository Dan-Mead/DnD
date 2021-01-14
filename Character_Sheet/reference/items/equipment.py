from Character_Sheet.reference.items.items_key import Item, Gear, Ammunition
from Character_Sheet.reference.items.jargon import *


# Magic.

class HolySymbol(Gear):
    name = "Holy Symbol"
    plural = 0


class ComponentPouch(Gear):
    name = "Component Pouch"
    plural = 2
    plural_actual = "Component Pouches"


class ArcaneFocus(Gear):
    name = "Arcane Focus"
    plural = 2
    plural_actual = "Arcane Foci"


class Spellbook(Gear):
    name = "Spellbook"
    plural = 0


class Arrow(Ammunition):
    name = "Arrow"
    plural = 0
