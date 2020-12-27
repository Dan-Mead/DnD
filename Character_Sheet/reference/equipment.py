from Character_Sheet.reference.proficiencies import *


# Types

class Ranged(Weapon):
    pass


class Melee(Weapon):
    pass


class Pack(Equipment):
    pass


class Magic(Equipment):
    pass


class Misc(Equipment):
    pass


class Ammo(Equipment):
    pass


class Tools(Equipment):
    pass


class GamingSet(Tools):
    name = "Gaming Set"
    plural = 0


class Instrument(Tools):
    name = "Musical Instrument"
    plural = 0


# Weapons

class Club(Simple, Melee):
    name = "Club"
    plural = 0


class Dagger(Simple, Melee):
    name = "Dagger"
    plural = 0


class Greatclub(Simple, Melee):
    name = "Greatclub"
    plural = 0


class Handaxe(Simple, Melee):
    name = "Handaxe"
    plural = 0


class Javelin(Simple, Melee):
    name = "Javelin"
    plural = 0


class LightHammer(Simple, Melee):
    name = "Light Hammer"
    plural = 0


class Mace(Simple, Melee):
    name = "Mace"
    plural = 0


class Quarterstaff(Simple, Melee):
    name = "Quarterstaff"
    plural = 0


class Sickle(Simple, Melee):
    name = "Sickle"
    plural = 0


class Spear(Simple, Melee):
    name = "Spear"
    plural = 0


class LightCrossbow(Simple, Ranged):
    name = "Light Crossbow"
    plural = 0


class Dart(Simple, Ranged):
    name = "Dart"
    plural = 0


class Shortbow(Simple, Ranged):
    name = "Shortbow"
    plural = 0


class Sling(Simple, Ranged):
    name = "Sling"
    plural = 0


class Battleaxe(Martial, Melee):
    name = "Battleaxe"
    plural = 0


class Flail(Martial, Melee):
    name = "Flail"
    plural = 0


class Glaive(Martial, Melee):
    name = "Glaive"
    plural = 0


class Greataxe(Martial, Melee):
    name = "Greataxe"
    plural = 0


class Greatsword(Martial, Melee):
    name = "Greatsword"
    plural = 0


class Halberd(Martial, Melee):
    name = "Halberd"
    plural = 0


class Lance(Martial, Melee):
    name = "Lance"
    plural = 0


class Longsword(Martial, Melee):
    name = "Longsword"
    plural = 0


class Maul(Martial, Melee):
    name = "Maul"
    plural = 0


class Morningstar(Martial, Melee):
    name = "Morningstar"
    plural = 0


class Pike(Martial, Melee):
    name = "Pike"
    plural = 0


class Rapier(Martial, Melee):
    name = "Rapier"
    plural = 0


class Shortsword(Martial, Melee):
    name = "Shortsword"
    plural = 0


class Scimitar(Martial, Melee):
    name = "Scimitar"
    plural = 0


class Shortsword(Martial, Melee):
    name = "Shortsword"
    plural = 0


class Trident(Martial, Melee):
    name = "Trident"
    plural = 0


class WarPick(Martial, Melee):
    name = "War Pick"
    plural = 0


class Warhammer(Martial, Melee):
    name = "Warhammer"
    plural = 0


class Whip(Martial, Melee):
    name = "Whip"
    plural = 0


class Blowgun(Martial, Ranged):
    name = "Blowgun"
    plural = 0


class HandCrossbow(Martial, Ranged):
    name = "Hand Crossbow"
    plural = 0


class HeavyCrossbow(Martial, Ranged):
    name = "Heavy Crossbow"
    plural = 0


class Longbow(Martial, Ranged):
    name = "Longbow"
    plural = 0


class Net(Martial, Ranged):
    name = "Net"
    plural = 0


# Other

class Arrow(Ammo):
    name = "Arrow"
    plural = 0


# Armour

class LeatherArmour(Light):
    name = "Leather Armour"
    plural = 1


class ChainMail(Heavy):
    name = "Chain Mail"
    plural = 1


class Shield(Shields):
    name = "Shield"
    plural = 0


# Magic.

class HolySymbol(Magic):
    name = "Holy Symbol"
    plural = 0


class ComponentPouch(Magic):
    name = "Component Pouch"
    plural = 2
    plural_actual = "Component Pouches"


class ArcaneFocus(Magic):
    name = "Arcane Focus"
    plural = 2
    plural_actual = "Arcane Foci"


class Spellbook(Magic):
    name = "Spellbook"
    plural = 0


# Packs

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


# Tools

class ThievesTools(Tools):
    name = "Thieves' Tools"
    plural = 1


class DiceSet(GamingSet):
    name = "Dice Set"
    plural = 0


class DragonchessSet(GamingSet):
    name = "Dragonchess Set"
    plural = 0


class PlayingCards(GamingSet):
    name = "Playing Card Set"
    plural = 0


class ThreeDragonAnte(GamingSet):
    name = "Three-Dragon Ante Set"
    plural = 0


class Bagpipes(Instrument):
    name = "Bagpipes"
    plural = 1


class Drum(Instrument):
    name = "Drum"
    plural = 0


class Dulcimer(Instrument):
    name = "Dulcimer"
    plural = 0


class Flute(Instrument):
    name = "Flute"
    plural = 0


class Horn(Instrument):
    name = "Horn"
    plural = 0


class Lute(Instrument):
    name = "Lute"
    plural = 0


class Lyre(Instrument):
    name = "Lyre"
    plural = 0


class PanFlute(Instrument):
    name = "Pan Flute"
    plural = 0


class Shawm(Instrument):
    name = "Shawm"
    plural = 0


class Viol(Instrument):
    name = "Viol"
    plural = 0


class TravellersClothes(Misc):
    name = "Traveller's Clothes"
    plural = 1


class Pouch(Misc):
    name = "Pouch"
    plural = 3
    plural_actual = "Pouches"


class Custom_Misc(Misc):
    def __init__(self, name, desc, plural=0, *plural_actual):
        self.name = name
        self.desc = desc
        self.plural = plural
        if plural == 3:
            self.plural_actual = plural_actual


if __name__ == '__main__':
    pass
