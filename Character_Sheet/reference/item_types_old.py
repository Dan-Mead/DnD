# from num2words import num2words
#
# def syntax(entry, num):
#     if not (isinstance(entry, (tuple, list))):
#         return entry.syntax_start(num) + entry.syntax_end(num)
#     elif len(entry) == 2:
#         return entry[0].syntax_start(num) + entry[1].syntax_end(num)
#     else:
#         return entry[0].syntax_start(num) + " ".join([item.name for item in entry[1:-1]]) + entry[1].syntax_end(num)
#
# class Item:
#
#
# ### Weapon Types
#
# class Weapon(Item):
#     name = "Weapon"
#     plural = 0
#
# class Martial(Weapon):
#     pass
#
# class Simple(Weapon):
#     pass
#
# class Ranged(Weapon):
#     pass
#
# class Melee(Weapon):
#     pass
#
# ### Armour Types
#
# class Armour(Item):
#     name = "Armour"
#     plural = 1
#
#
# class Light(Armour):
#     name = "Light"
#
#
# class Medium(Armour):
#     name = "Medium"
#
#
# class Heavy(Armour):
#     name = "Heavy"
#
#
# class Shields(Armour):
#     name = "Shields"
#
# ### Tool Types
#
# class Tool(Item):
#     name = "Tool"
#     plural = 0
#
# class ArtisanTools(Tool):
#     name = "Artisan's tools"
#     plural = 1
#
# class GamingSet(Tool):
#     name = "Gaming Set"
#     plural = 0
#
# class Instrument(Tool):
#     name = "Musical Instrument"
#     plural = 0
#
# ### Other Types
# class Pack(Item):
#     pass
#
#
# class Magic(Item):
#     pass
#
#
# class Misc(Item):
#     pass
#
#
# class Ammo(Item):
#     pass
#
#
# if __name__ == '__main__':
#     pass
