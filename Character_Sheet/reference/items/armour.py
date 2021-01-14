from Character_Sheet.reference.items.items_key import Item, Armour
from Character_Sheet.reference.items.jargon import *

class Light(Armour):
    name = "Light"
    suffix = "Armour"
    plural = 1


class Medium(Armour):
    name = "Medium"
    suffix = "Armour"
    plural = 1

class Heavy(Armour):
    name = "Heavy"
    suffix = "Armour"
    plural = 1

class Shields(Armour):
    name = "Shields"
    plural = 2
    plural_actual = "Shields"


class LeatherArmour(Light):
    name = "Leather Armour"
    plural = 1

class HideArmour(Medium):
    name = "Hide Armour"
    plural = 1


class ChainMail(Heavy):
    name = "Chain Mail"
    plural = 1

class Shield(Shields):
    name = "Shield"
    plural = 0
