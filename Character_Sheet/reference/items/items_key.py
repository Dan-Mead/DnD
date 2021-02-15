from num2words import num2words
from Character_Sheet import helpers as helpers
from Character_Sheet.reference.items.jargon import *


class Types:
    weapon = "weapon"
    armour = "armour"
    ammunition = "ammunition"
    tool = "tools"
    potions = "potions"
    gear = "gear"
    pack = "pack"
    container = "container"
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

    wieldable = False

    def __init__(self, num, name=None):
        self.num = num
        if name:
            self.name = name

    # def __repr__(self):
    #     return repr(self.name)

    @classmethod
    def uncountable(cls):

        if hasattr(cls, "suffix") and cls.__subclasses__():
            suffix = " " + cls.suffix
        else:
            suffix = ""

        if cls.plural == 0:
            return f"{cls.name + suffix}s"
        elif cls.plural == 1:
            return f"{cls.name + suffix}"
        elif cls.plural == 2:
            return f"{cls.plural_actual + suffix}"

    @classmethod
    def syntax_start(cls, num=None):

        if not num:
            num = cls.num

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
    def syntax_end(cls, num=None):

        if not num:
            num = cls.num

        if hasattr(cls, "suffix") and cls.__subclasses__():
            suffix = " " + cls.suffix
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

    # @classmethod
    def syntax(self, num=None):

        if not num:
            num = self.num
        name = self.name

        if hasattr(self, "suffix") and self.__class__.__subclasses__():
            name += " " + self.suffix

        if self.plural == 0:
            if num == 1:
                if name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {name}".lower()
                else:
                    return f"a {name}".lower()
            else:
                return f"{num2words(num)} {name}s".lower()
        elif self.plural == 1:
            if num == 1:
                return f"{name}".lower()
            else:
                return f"{num2words(num)} sets of {name}".lower()
        elif self.plural == 2:
            if num == 1:
                if name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {name}".lower()
                else:
                    return f"a {name}".lower()
            else:
                return f'{num2words(num)} {self.plural_actual}'.lower()

    Types = Types
    Proficiencies = Proficiencies


class Weapon(Item):

    wieldable = True
    equippable = False

    item_type = Item.Types.weapon

    class PropertyKeys:

        finesse = "finesse"
        heavy = "heavy"
        light = "light"
        loading = "loading"
        reach = "reach"
        special = "special"
        two_handed = "two_handed"
        improvised = "improvised"
        silvered = "silvered"

        @staticmethod
        def thrown(range_min, range_max):
            range = f"{range_min}/{range_max}"
            return "thrown", ("range", range)

        @staticmethod
        def versatile(dmg_num, dmg_val):
            return (("versatile", (dmg_num, dmg_val)),)

        @staticmethod
        def ammunition(range_min, range_max):
            range = (range_min, range_max)
            return "ammunition", ("range", range)

        @staticmethod
        def special(desc):
            return (("special", desc),)

    @staticmethod
    def properties(*args):

        dict = {}

        if len(args) == 1:
            args = (args)
        for arg in args:
            if isinstance(arg, str):
                dict[arg] = None
            else:
                for a in arg:
                    if isinstance(a, str):
                        dict[a] = None
                    else:
                        dict[a[0]] = a[1]

        return dict

class Armour(Item):
    equippable = True
    item_type = Item.Types.armour


class Ammunition(Item):
    equippable = True
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


class Container(Item):
    item_type = Item.Types.container

    def __init__(self, num, *contents):
        self.contents = contents
        contents = [item.name for item in self.contents]
        contents_list = helpers.list_syntax(contents)
        self.num = num,
        super().__init__(num, self.name)
        self.name = F"{self.name} containing {contents_list}."

class Other(Item):
    item_type = Item.Types.other


class Notable(Item):
    item_type = Item.Types.notable
