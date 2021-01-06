from num2words import num2words

def syntax(entry, num):
    if not (isinstance(entry, (tuple, list))):
        return entry.syntax_start(num) + entry.syntax_end(num)
    elif len(entry) == 2:
        return entry[0].syntax_start(num) + entry[1].syntax_end(num)
    else:
        return entry[0].syntax_start(num) + " ".join([item.name for item in entry[1:-1]]) + entry[1].syntax_end(num)

class Item:

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
        if cls.plural == 0:
            if num == 1:
                return f"{cls.name}".lower()
            else:
                return f"{cls.name}s".lower()
        elif cls.plural == 1:
            return f"{cls.name}".lower()
        elif cls.plural == 2:
            return f'{num2words(num)} {cls.plural_actual}'.lower()

    @classmethod
    def syntax(cls, num):
        if cls.plural == 0:
            if num == 1:
                if cls.name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {cls.name}".lower()
                else:
                    return f"a {cls.name}".lower()
            else:
                return f"{num2words(num)} {cls.name}s".lower()
        elif cls.plural == 1:
            if num == 1:
                return f"{cls.name}".lower()
            else:
                return f"{num2words(num)} sets of {cls.name}".lower()
        elif cls.plural == 2:
            if num == 1:
                if cls.name[0].lower() in ["a", "e", "i", "o", "u", "h"]:
                    return f"an {cls.name}".lower()
                else:
                    return f"a {cls.name}".lower()
            else:
                return f'{num2words(num)} {cls.plural_actual}'.lower()

### Weapon Types

class Weapon(Item):
    name = "Weapon"
    plural = 0

class Martial(Weapon):
    pass

class Simple(Weapon):
    pass

class Ranged(Weapon):
    pass

class Melee(Weapon):
    pass

### Armour Types

class Armour(Item):
    name = "Armour"
    plural = 1


class Light(Armour):
    name = "Light"


class Medium(Armour):
    name = "Medium"


class Heavy(Armour):
    name = "Heavy"


class Shields(Armour):
    name = "Shields"

### Tool Types

class Tool(Item):
    name = "Tool"
    plural = 0

class ArtisanTools(Tool):
    name = "Artisan's tools"
    plural = 1

class GamingSet(Tool):
    name = "Gaming Set"
    plural = 0

class Instrument(Tool):
    name = "Musical Instrument"
    plural = 0

### Other Types
class Pack(Item):
    pass


class Magic(Item):
    pass


class Misc(Item):
    pass


class Ammo(Item):
    pass


if __name__ == '__main__':
    pass
