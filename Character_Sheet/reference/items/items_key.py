from num2words import num2words
from Character_Sheet.reference.items.jargon import *


class Types:
    weapon = "weapon"
    armour = "armour"
    ammunition = "ammunition"
    tool = "tools"
    potions = "potions"
    gear = "gear"
    pack = "pack"
    misc = "misc"
    other = "other"
    notable = "notable"


class Proficiencies:
    simple = "simple"
    martial = "martial"
    light = "light"
    medium = "medium"
    heavy = "heavy"
    shields = "shields"

    lookup = {simple: Types.weapon,
              martial: Types.weapon,
              light: Types.armour,
              medium: Types.armour,
              heavy: Types.armour,
              shields: Types.armour
              }


class Item:

    def __init__(self, name=None):
        if name:
            self.name = name

    def __repr__(self):
        return repr(self.name)

    @classmethod
    def uncountable(cls):

        if hasattr(cls, "suffix") and cls.__subclasses__():
            suffix = " "+cls.suffix
        else:
            suffix = ""

        if cls.plural == 0:
            return f"{cls.name + suffix}s"
        elif cls.plural == 1:
            return f"{cls.name + suffix}"
        elif cls.plural == 2:
            return f"{cls.plural_actual + suffix}"

    @classmethod
    def syntax_start(cls, num):
        if cls.plural == 0 or cls.plural == 2:
            if num == 1:
                if cls.name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {cls.name}".lower()
                else:
                    return f"a {cls.name}".lower()
            else:
                return f"{num2words(num)} {cls.name}".lower()
        elif cls.plural == 1:
            if num == 1:
                return f"a set of {cls.name}".lower()
            else:
                return f"{num2words(num)} sets of {cls.name}"

    @classmethod
    def syntax_end(cls, num):

        if hasattr(cls, "suffix") and cls.__subclasses__():
            suffix = " "+cls.suffix
        else:
            suffix = ""

        if cls.plural == 0:
            if num == 1:
                return f"{cls.name + suffix}".lower()
            else:
                return f"{cls.name + suffix}s".lower()
        elif cls.plural == 1:
            return f"{cls.name + suffix}".lower()
        elif cls.plural == 2:
            return f'{num2words(num)} {cls.plural_actual}'.lower()

    @classmethod
    def syntax(cls, num):

        name = cls.name

        if hasattr(cls, "suffix") and cls.__subclasses__():
            name += " "+cls.suffix

        if cls.plural == 0:
            if num == 1:
                if name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {name}".lower()
                else:
                    return f"a {name}".lower()
            else:
                return f"{num2words(num)} {name}s".lower()
        elif cls.plural == 1:
            if num == 1:
                return f"{name}".lower()
            else:
                return f"{num2words(num)} sets of {name}".lower()
        elif cls.plural == 2:
            if num == 1:
                if name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {name}".lower()
                else:
                    return f"a {name}".lower()
            else:
                return f'{num2words(num)} {cls.plural_actual}'.lower()

    Types = Types
    Proficiencies = Proficiencies


class Weapon(Item):
    item_type = Item.Types.weapon

    def __init__(self):
        super().__init__(name=self.name)

    class PropertyKeys:

        finesse = "finesse"
        heavy = "heavy"
        light = "light"
        loading = "loading"
        reach = "reach"
        special = "special"
        two_handed = "two_handed"
        versatile = "versatile"
        improvised = "improvised"
        silvered = "silvered"

        @staticmethod
        def thrown(range_min, range_max):
            range = f"{range_min}/{range_max}"
            return "thrown"

    @staticmethod
    def properties(*args):

        if len(args) == 1:
            return (args)
        else:
            return args


class Armour(Item):
    item_type = Item.Types.armour


class Ammunition(Item):
    item_type = Item.Types.ammunition


class Gear(Item):
    item_type = Item.Types.gear


class Tool(Item):
    item_type = Item.Types.tool


class Potions(Item):
    item_type = Item.Types.potions


class Misc(Item):
    item_type = Item.Types.misc


class Pack(Item):
    item_type = Item.Types.pack


class Other(Item):
    item_type = Item.Types.other


class Notable(Item):
    item_type = Item.Types.notable
