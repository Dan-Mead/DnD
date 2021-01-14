from Character_Sheet.reference.items.items_key import Item, Misc, Pack


class Custom_Misc(Misc):
    def __init__(self, name, desc, plural=0, *plural_actual):
        self.name = name
        self.desc = desc
        self.plural = plural
        if plural == 3:
            self.plural_actual = plural_actual


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


### Misc

class TravellersClothes(Misc):
    name = "Traveller's Clothes"
    plural = 1


class Pouch(Misc):
    name = "Pouch"
    plural = 2
    plural_actual = "Pouches"
