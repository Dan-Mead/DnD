import inspect
import sys

class race:
    # def __init__(self, name, speed, size):
    #     self.name = name
    #     self.speed = speed
    #     self.size = size
    pass
class subrace:
    pass

class Human(race):
    name = "Human"
    speed = 30
    size = "Medium"
    languages = ("Common", "Choice")
    @staticmethod
    def prereq():
        return False

class Human_base(Human):
    subrace_name = "Base"
    from glossary import attrs
    ASI = tuple(zip(attrs, [1]*len(attrs)))

class Human_variant(Human):
    subrace_name = "Variant"
    ASI = (("Choice", "Any"), ("Choice", "Any"))

class Half_Orc(race):
    name = "Half-Orc"
    speed = 60
    size = "Medium"
    languages = ("Common", "Orc")
    ASI = (("STR", +2), ("CON", +1))

race_list = dict([(race.name, race) for race in race.__subclasses__()])

# race_list = dict(zip())

# for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
#
#
#
#     print(name, obj)
#     print(issubclass(obj, race))