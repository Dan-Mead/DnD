from helper_functions import LDK

class Effect():

    ## TODO: Need to be able to remove as well

    def add_effect(self, char):

        path_string = self.aspect.split(".")
        path = LDK(char, path_string)
        path[self.origin] += [self.value]

class Modifier(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value
            

class Note(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value


class Feature(Effect):
        def __init__(self, origin, aspect, value):
                self.origin = origin
                self.aspect = aspect
                self.value = value






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
        self.silvered = False
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