from Character_Sheet.reference.item_types import *


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


###### Tools

### Artisan Tools

class Alchemist(ArtisanTools):
    name = "Alchemist's Supplies"
    plural = 1


class Brewer(ArtisanTools):
    name = "Brewer's Supplies"
    plural = 1


class Calligrapher(ArtisanTools):
    name = "Calligrapher's Supplies"
    plural = 1


class Carpenter(ArtisanTools):
    name = "Carpenter's Tools"
    plural = 1


class Cartographer(ArtisanTools):
    name = "Cartographer's Tools"
    plural = 1


class Cobbler(ArtisanTools):
    name = "Cobbler's Tools"
    plural = 1


class Glassblower(ArtisanTools):
    name = "Glassblower's tools"
    plural = 1


class Jeweler(ArtisanTools):
    name = "Jeweler's tools"
    plural = 1


class Leatherworker(ArtisanTools):
    name = "Leatherworker's tools"
    plural = 1


class Mason(ArtisanTools):
    name = "Mason's tools"
    plural = 1


class Painter(ArtisanTools):
    name = "Painter's Supplies"
    plural = 1


class Potter(ArtisanTools):
    name = "Potter's Tools"
    plural = 1


class Smith(ArtisanTools):
    name = "Smith's tools"
    plural = 1


class Tinker(ArtisanTools):
    name = "Tinker's tools"
    plural = 1


class Weaver(ArtisanTools):
    name = "Weaver's Tools"
    plural = 1


class Woodcarver(ArtisanTools):
    name = "Woodcarver's"
    plural = 1


### Gaming Sets

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


### Musical Instruments

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


### Other Tools


class Disguise(Tool):
    name = "Disguise kit"
    plural = True


class Forgery(Tool):
    name = "Forgery kit"
    plural = True


class Herbalism(Tool):
    name = "Herbalism kit"
    plural = True


class Navigator(Tool):
    name = "Navigator's tools"
    plural = 1


class Poisoner(Tool):
    name = "Poisoner's kit"
    plural = 0


class ThievesTools(Tool):
    name = "Thieves' Tools"
    plural = 1


### Misc

class TravellersClothes(Misc):
    name = "Traveller's Clothes"
    plural = 1


class Pouch(Misc):
    name = "Pouch"
    plural = 2
    plural_actual = "Pouches"
