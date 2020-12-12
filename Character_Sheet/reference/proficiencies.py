from num2words import num2words


def syntax(entry, num):
    if not (isinstance(entry, (tuple, list))):
        return entry.syntax_start(num) + entry.syntax_end(num)
    elif len(entry) == 2:
        return entry[0].syntax_start(num) + entry[1].syntax_end(num)
    else:
        return entry[0].syntax_start(num) + " ".join([item.name for item in entry[1:-1]]) + entry[1].syntax_end(num)

class Equipment:

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
        elif cls.plural ==2:
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



class Weapon(Equipment):
    name = "Weapon"
    plural = True


class Martial(Weapon):
    name = "Martial"
    plural = True


class Simple(Weapon):
    name = "Simple"
    plural = True


class Armour(Equipment):
    name = "Armour"
    plural = False

class Light(Armour):
    name = "Light"
    plural = False

class Medium(Armour):
    name = "Medium"
    plural = False

class Heavy(Armour):
    name = "Heavy"
    plural = False

class Shields(Armour):
    name = "Shields"
    plural = True

class Tools:
    plural = False

class Thieves(Tools):
    name = "Thieves' tools"

if __name__ == '__main__':
    pass
