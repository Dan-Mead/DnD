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

### Actual Values

class LeatherArmour(Light):
    name = "Leather Armour"
    plural = 1
    cost = gp(10)
    AC = 11
    STR = None
    stealth_dis = False
    weight = 10

class HideArmour(Medium):
    name = "Hide Armour"
    plural = 1
    cost = gp(10)
    AC = 12
    STR = None
    stealth_dis = False
    weight = 12


class ChainMail(Heavy):
    name = "Chain Mail"
    plural = 1
    cost = gp(75)
    AC = 16
    STR = 13
    stealth_dis = True
    weight = 55

class Shield(Shields):
    wieldable = True
    name = "Shield"
    plural = 0
    cost = gp(10)
    STR = None
    stealth_dis = False
    weight = 6
