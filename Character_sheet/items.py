import inspect
import sys


def get_items(type_filter=None):
    item_types = Item.__subclasses__()

    if type_filter:
        filter_val = getattr(sys.modules[__name__], type_filter)
        items = {}
        for item in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if filter_val in item[1].__bases__:
                items[item[0]] = item[1]
    else:
        items = {}
        for item in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if item[1] not in item_types:
                items[item[0].replace("_", " ")] = item[1]

    return items


def get_item(item_name, num):
    items = get_items()

    item = items[item_name](num)

    return item


class Item:

    def __init__(self, num):
        self.num = num
        cost = self.cost
        self.cost = int(self.cost.split(" ")[0]), self.cost.split(" ")[1] + "p"

    def add_number(self, num):
        self.num += num


class Weapon(Item):
    dmg_type = {'b': 'Bludgeoning',
                's': 'Slashing',
                'p': 'Piercing'}

    def __init__(self, num):
        self.equippable = True, 'Hand'
        self.type = 'Weapon'
        self.weapon_type = self.get_weapon_type()
        self.dmg_type = self.dmg_type[self.dmg[2]]
        self.dmg = self.dmg[0], self.dmg[1]
        super().__init__(num)

    def silver(self):
        print(type(self.properties))
        if type(self.properties) == str:
            self.properties = (self.properties,) + ('Silvered',)
        else:
            self.properties += ('Silvered',)

    def attack(self):
        pass  # TODO Remember Profficiencies


class Armor(Item):

    def __init__(self, num):
        self.equippable = True, 'Body'
        self.type = 'Armor'
        super().__init__(num)


class Pack:
    def __init__(self):
        pass

    def unpack(self):
        pass


class Other(Item):
    def __init__(self, num):
        super().__init__(num)


class Misc_Object(Item):
    def __init__(self, num):
        self.num = num
        self.cost = None


############################################################ Weapons

class Club(Weapon):
    def __init__(self, num):
        self.dmg = 1, 4, 'b'
        self.properties = 'Light'
        self.cost = '1 s'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Dagger(Weapon):
    def __init__(self, num):
        self.dmg = 1, 4, 'p'
        self.properties = 'Finesse', 'Light', 'Thrown 20/60'
        self.cost = '2 g'
        self.weight = 1
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Greatclub(Weapon):
    def __init__(self, num):
        self.dmg = 1, 8, 'b'
        self.properties = 'Two-handed'
        self.cost = '2 s'
        self.weight = 10
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Handaxe(Weapon):
    def __init__(self, num):
        self.dmg = 1, 6, 's'
        self.properties = 'Light', 'Thrown, 20/60'
        self.cost = '5 g'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Javelin(Weapon):
    def __init__(self, num):
        self.dmg = 1, 6, 'p'
        self.properties = 'Thrown, 30/120'
        self.cost = '5 s'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Light_Hammer(Weapon):
    def __init__(self, num):
        self.dmg = 1, 4, 'b'
        self.properties = 'Light', 'Thrown 20/60'
        self.cost = '2 g'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Mace(Weapon):
    def __init__(self, num):
        self.dmg = 1, 6, 'b'
        self.properties = None
        self.cost = '5 g'
        self.weight = 4
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Quarterstaff(Weapon):
    def __init__(self, num):
        self.dmg = 1, 6, 'b'
        self.properties = 'Versatile 8'
        self.cost = '2 s'
        self.weight = 4
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Sickle(Weapon):
    def __init__(self, num):
        self.dmg = 1, 4, 's'
        self.properties = 'Light'
        self.cost = '1 g'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


class Spear(Weapon):
    def __init__(self, num):
        self.dmg = 1, 6, 'p'
        self.properties = 'Thrown 20/60', 'Versatile 8'
        self.cost = '1 g'
        self.weight = 3
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Simple', 'Melee'


##################### Martial Melee

class Battleaxe(Weapon):
    def __init__(self, num):
        self.cost = '10 g'
        self.dmg = 1, 8, 's'
        self.weight = 4
        self.properties = 'Versatile 10'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Flail(Weapon):
    def __init__(self, num):
        self.cost = '10 g'
        self.dmg = 1, 8, 'b'
        self.weight = 2
        self.properties = None
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Glaive(Weapon):
    def __init__(self, num):
        self.cost = '20 g'
        self.dmg = 1, 10, 's'
        self.weight = 6
        self.properties = 'Heavy', 'Reach', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Greataxe(Weapon):
    def __init__(self, num):
        self.cost = '30 g'
        self.dmg = 1, 12, 's'
        self.weight = 7
        self.properties = 'Heavy', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Greatsword(Weapon):
    def __init__(self, num):
        self.cost = '50 g'
        self.dmg = 2, 6, 's'
        self.weight = 6
        self.properties = 'Heavy', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Halberd(Weapon):
    def __init__(self, num):
        self.cost = '20 g'
        self.dmg = 1, 10, 's'
        self.weight = 6
        self.properties = 'Heavy', 'Reach', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Lance(Weapon):
    def __init__(self, num):
        self.cost = '10 g'
        self.dmg = 1, 12, 'p'
        self.weight = 6
        self.properties = 'Reach', 'Special'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Longsword(Weapon):
    def __init__(self, num):
        self.cost = '15 g'
        self.dmg = 1, 8, 's'
        self.weight = 3
        self.properties = 'Versatile 10'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Maul(Weapon):
    def __init__(self, num):
        self.cost = '10 g'
        self.dmg = 2, 6, 'b'
        self.weight = 10
        self.properties = 'Heavy', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Morningstar(Weapon):
    def __init__(self, num):
        self.cost = '15 g'
        self.dmg = 1, 8, 'p'
        self.weight = 4
        self.properties = None
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Pike(Weapon):
    def __init__(self, num):
        self.cost = '5 g'
        self.dmg = 1, 10, 'p'
        self.weight = 18
        self.properties = 'Heavy', 'Reach', 'Two-handed'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Rapier(Weapon):
    def __init__(self, num):
        self.cost = '25 g'
        self.dmg = 1, 8, 'p'
        self.weight = 2
        self.properties = 'Finesse'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Scimitar(Weapon):
    def __init__(self, num):
        self.cost = '25 g'
        self.dmg = 1, 6, 's'
        self.weight = 3
        self.properties = 'Finesse', 'Light'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Shortsword(Weapon):
    def __init__(self, num):
        self.cost = '10 g'
        self.dmg = 1, 6, 'p'
        self.weight = 2
        self.properties = 'Finesse', 'Light'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Trident(Weapon):
    def __init__(self, num):
        self.cost = '5 g'
        self.dmg = 1, 6, 'p'
        self.weight = 4
        self.properties = 'Thrown 20/60', 'Versatile 8'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class War_Pick(Weapon):
    def __init__(self, num):
        self.cost = '5 g'
        self.dmg = 1, 8, 'p'
        self.weight = 2
        self.properties = None
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Warhammer(Weapon):
    def __init__(self, num):
        self.dmg = 1, 8, 'b'
        self.properties = 'Versatile 10'
        self.cost = '15 g'
        self.weight = 2
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


class Whip(Weapon):
    def __init__(self, num):
        self.cost = '2 g'
        self.dmg = 1, 4, 's'
        self.weight = 3
        self.properties = 'Finesse', 'Reach'
        super().__init__(num)

    @staticmethod
    def get_weapon_type():
        return 'Martial', 'Melee'


############################################################ Armor

class Padded(Armor):
    def __init__(self, num):
        self.desc = 'Padded armor consists of quilted layers of cloth and batting.'
        self.armor_type = 'Light'
        self.AC = 11
        self.req = None
        self.stealth_dis = True
        self.cost = '5 g'
        self.weight = 8
        super().__init__(num)


class Leather(Armor):
    def __init__(self, num):
        self.desc = 'The Breastplate and shoulder protectors of this armor are made of leather that has been ' \
                    'stiffened by being boiled in oil. The rest of the armor is made of softer and more flexible ' \
                    'materials. '
        self.armor_type = 'Light'
        self.cost = '5 g'
        self.AC = 11
        self.req = None
        self.stealth_dis = False
        self.weight = 10
        super().__init__(num)


class Studded_Leather(Armor):
    def __init__(self, num):
        self.desc = 'Made from tough but flexible leather, studded leather is reinforced with close-set rivets or ' \
                    'spikes. '
        self.armor_type = 'Light'
        self.cost = '45 g'
        self.AC = 12
        self.req = None
        self.stealth_dis = False
        self.weight = 13
        super().__init__(num)


class Hide(Armor):
    def __init__(self, num):
        self.desc = 'This crude armor consists of thick furs and pelts. It is commonly worn by Barbarian tribes, ' \
                    'evil Humanoids, and other folk who lack access to the tools and materials needed to create ' \
                    'better armor. '
        self.armor_type = 'Medium'
        self.cost = '10 g'
        self.AC = 12
        self.req = None
        self.stealth_dis = False
        self.weight = 12
        super().__init__(num)


class Chain_Shirt(Armor):
    def __init__(self, num):
        self.desc = 'Made of interlocking metal rings, a Chain Shirt is worn between layers of clothing or leather. ' \
                    'This armor offers modest Protection to the wearer’s upper body and allows the sound of the rings ' \
                    'rubbing against one another to be muffled by outer layers. '
        self.armor_type = 'Medium'
        self.cost = '50 g'
        self.AC = 13
        self.req = None
        self.stealth_dis = False
        self.weight = 20
        super().__init__(num)


class Scale_Mail(Armor):
    def __init__(self, num):
        self.desc = 'This armor consists of a coat and leggings (and perhaps a separate skirt) of leather covered ' \
                    'with overlapping pieces of metal, much like the scales of a fish. The suit includes gauntlets. '
        self.armor_type = 'Medium'
        self.cost = '50 g'
        self.AC = 14
        self.req = None
        self.stealth_dis = True
        self.weight = 45
        super().__init__(num)


class Breastplate(Armor):
    def __init__(self, num):
        self.desc = 'This armor consists of a fitted metal chest piece worn with supple leather. Although it leaves ' \
                    'the legs and arms relatively unprotected, this armor provides good Protection for the wearer’s ' \
                    'vital organs while leaving the wearer relatively unencumbered. '
        self.armor_type = 'Medium'
        self.cost = '400 g'
        self.AC = 14
        self.req = None
        self.stealth_dis = False
        self.weight = 20
        super().__init__(num)


class Half_Plate(Armor):
    def __init__(self, num):
        self.desc = 'Half Plate consists of shaped metal plates that cover most of the wearer’s body. It does not ' \
                    'include leg Protection beyond simple greaves that are attached with leather straps. '
        self.armor_type = 'Medium'
        self.cost = '750 g'
        self.AC = 15
        self.req = None
        self.stealth_dis = True
        self.weight = 40
        super().__init__(num)


class Ring_Mail(Armor):
    def __init__(self, num):
        self.desc = "This armor is Leather Armor with heavy rings sewn into it. The rings help reinforce the armor " \
                    "against blows from Swords and axes. Ring Mail is inferior to Chain Mail, and it's usually worn " \
                    "only by those who can’t afford better armor. "
        self.armor_type = 'Heavy'
        self.AC = 14
        self.req = None
        self.stealth_dis = True
        self.cost = '30 g'
        self.weight = 40
        super().__init__(num)


class Chain_Mail(Armor):
    def __init__(self, num):
        self.desc = 'Made of interlocking metal rings, chain mail includes a layer of quilted fabric worn underneath ' \
                    'the mail to prevent chafing and to cushion the impact of blows. The suit includes gauntlets. '
        self.armor_type = 'Heavy'
        self.AC = 16
        self.req = 13
        self.stealth_dis = True
        self.cost = '75 g'
        self.weight = 55
        super().__init__(num)


class Splint(Armor):
    def __init__(self, num):
        self.desc = 'This armor is made of narrow vertical strips of metal riveted to a backing of leather that is ' \
                    'worn over cloth padding. Flexible Chain Mail protects the joints. '
        self.armor_type = 'Heavy'
        self.AC = 17
        self.req = 15
        self.stealth_dis = True
        self.cost = '200 g'
        self.weight = 60
        super().__init__(num)


class Plate(Armor):
    def __init__(self, num):
        self.desc = 'Plate consists of shaped, interlocking metal plates to cover the entire body. A suit of plate ' \
                    'includes gauntlets, heavy leather boots, a visored helmet, and thick layers of padding ' \
                    'underneath the armor. Buckles and straps distribute the weight over the body. '
        self.armor_type = 'Heavy'
        self.AC = 18
        self.req = 15
        self.stealth_dis = True
        self.cost = '1500 g'
        self.weight = 65
        super().__init__(num)


class Shield(Armor):
    def __init__(self, num):
        self.desc = 'A shield is made from wood or metal and is carried in one hand. Wielding a shield increases your ' \
                    'Armor Class by 2. You can benefit from only one shield at a time. '
        self.armor_type = 'Shield'
        self.AC = 2
        self.req = None
        self.stealth_dis = False
        self.cost = '10 g'
        self.weight = 6
        super().__init__(num)
        self.equippable = True, 'Hand'


############################################################ Packs

class Explorer_Pack(Pack):
    def __init__(self, num):
        self.contents = {
            "Backpack": Misc_Object(1),
            "Bedroll": Misc_Object(1),
            "Mess Kit": Misc_Object(1),
            "Tinderbox": Misc_Object(1),
            "Torches": Misc_Object(10),
            "Rations": Misc_Object(10),
            "Waterskin": Misc_Object(1),
            "Rope": Misc_Object(1)
        }


class Priest_Pack(Pack):
    def __init__(self, num):
        self.contents = {
            "Backpack": Misc_Object(1),
            "Blanket": Misc_Object(1),
            "Candles": Misc_Object(10),
            "Tinderbox": Misc_Object(1),
            "Alms Box": Misc_Object(1),
            "Incense Block": Misc_Object(2),
            "Censer": Misc_Object(1),
            "Vestments": Misc_Object(1),
            "Rations": Misc_Object(2),
            "Waterskin": Misc_Object(1)
        }


############################################################ Misc

class Holy_Symbol(Other):
    def __init__(self, num):
        self.desc = 'A holy symbol is a representation of a god or pantheon. A cleric or paladin can use a holy ' \
                    'symbol as a spellcasting focus, as described in the Spellcasting section. To use the symbol in ' \
                    'this way, the caster must hold it in hand, wear it visibly, or bear it on a shield. '
        self.cost = '5 g'
        super().__init__(num)
