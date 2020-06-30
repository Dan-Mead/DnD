def get_item(item_name, num):
    item_list = {
        "Warhammer" : Warhammer,
        "Handaxe" : Handaxe,
        "Javelin" : Javelin,

        "Shield" : Shield,
        "Chain Mail" : Chain_Mail,

        "Explorer's Pack" : Explorer_Pack,

        "Holy Symbol" : Holy_Symbol,
    }
    
    item = item_list[item_name](num)

    if Pack in type(item).__bases__:
        item = item.contents ### TODO: Probably put this in some unpacking code.

    return item


class Item:

    def __init__(self, num):
        self.num = num
        cost = self.cost
        self.cost = int(self.cost.split(" ")[0]), self.cost.split(" ")[1]+"p"

    def add_item(self, num):
        self.num += num

class Weapon(Item):

    dmg_type = {'b' : 'Bludgeoning',
               's' : 'Slashing',
               'p' : 'Piercing'}

    def __init__(self, num):
        self.equippable = True, 'Hand'
        self.type = 'Weapon'
        self.dmg_type = self.dmg_type[self.dmg[2]]
        self.dmg = self.dmg[0], self.dmg[1]
        super().__init__(num)
    
    def attack(self):
        pass ## TODO Remember Profficiencies

class Armor(Item):

    def __init__(self, num):
        self.equippable = True, 'Body'
        self.type = 'Armor'
        super().__init__(num)

class Pack:
    def __init__(self):
        pass

############################################################ Weapons

class Warhammer(Weapon):
    def __init__(self, num):
        self.weapon_type = 'Martial', 'Melee'
        self.dmg = 1, 8, 'b'
        self.properties = 'Versatile, 1d10'
        self.cost = '15 g'
        self.weight = 2
        super().__init__(num)

class Handaxe(Weapon):
    def __init__(self, num):
        self.weapon_type = 'Simple', 'Melee'
        self.dmg = 1, 6, 's'
        self.properties = 'Light', 'Thrown, 20/60'
        self.cost = '5 g'
        self.weight = 2
        super().__init__(num)

class Javelin(Weapon):
    def __init__(self, num):
        self.weapon_type = 'Simple', 'Melee'
        self.dmg = 1, 6, 'p'
        self.properties = 'Thrown, 30/120'
        self.cost = '5 s'
        self.weight = 2
        super().__init__(num)   

############################################################ Armor

class Shield(Armor):
    def __init__(self, num):
        self.desc = 'A shield is made from wood or metal and is carried in one hand. Wielding a shield increases your Armor Class by 2. You can benefit from only one shield at a time.'
        self.armor_type = 'Shield'
        self.AC = 2
        self.req = None
        self.stealth_dis = False
        self.cost = '10 g'
        self.weight = 6
        super().__init__(num)
        self.equippable = True, 'Hand'

class Chain_Mail(Armor):
    def __init__(self, num):
        self.desc = 'Made of interlocking metal rings, chain mail includes a layer of quilted fabric worn underneath the mail to prevent chafing and to cushion the impact of blows. The suit includes gauntlets.'
        self.armor_type = 'Heavy'
        self.AC = 16
        self.req = 13
        self.stealth_dis = True
        self.cost = '75 g'
        self.weight = 55
        super().__init__(num)


############################################################ Packs

class Explorer_Pack(Pack):
    def __init__(self, num):
        self.contents = {
            "Backpack" : Misc_Object(1),
            "Bedroll" : Misc_Object(1),
            "Mess Kit" : Misc_Object(1),
            "Tinderbox" : Misc_Object(1),
            "Torches" : Misc_Object(10),
            "Rations" : Misc_Object(10),
            "Waterskin" : Misc_Object(1),
            "Rope" : Misc_Object(1)
        }

############################################################ Misc

class Holy_Symbol(Item):
    def __init__(self, num):
        self.desc = 'A holy symbol is a representation of a god or pantheon. A cleric or paladin can use a holy symbol as a spellcasting focus, as described in the Spellcasting section. To use the symbol in this way, the caster must hold it in hand, wear it visibly, or bear it on a shield.'
        self.cost = '5 g'
        super().__init__(num)

class Misc_Object:
    def __init__(self, num):
        self.num = num

item = get_item("Explorer's Pack", 1)

print("Done!")