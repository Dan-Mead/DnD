from Character_Sheet.reference.items.items_key import Item, Misc, Pack, Container
from Character_Sheet.reference.items.jargon import *

class Custom_Misc(Misc):
    def __init__(self, num, name, desc, plural=0, *plural_actual):
        self.name = name
        self.desc = desc
        self.plural = plural
        if plural == 3:
            self.plural_actual = plural_actual
        super().__init__(num, name)

    def rename(self, new_name):
        self.name = new_name
    def change_description(self, new_desc):
        self.desc = new_desc

### Packs

class PriestPack(Pack):
    name = "Priest's Pack"
    plural = 0


class ExplorerPack(Pack):
    name = "Explorer's Pack"
    plural = 0


class BurglarPack(Pack):
    name = "Burglar's Pack"
    plural = 0


class DungeoneerPack(Pack):
    name = "Dungeoneer's Pack"
    plural = 0


class ScholarPack(Pack):
    name = "Scholar's Pack"
    plural = 0

### Containers

class Pouch(Container):
    name = "Pouch"
    plural = 2
    plural_actual = "Pouches"

### Misc

class TravellersClothes(Misc):
    name = "Traveller's Clothes"
    plural = 1
    cost = gp(2)
    weight = 4


