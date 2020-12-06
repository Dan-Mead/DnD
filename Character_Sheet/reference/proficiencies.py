class Equipment:
    pass


class Weapon(Equipment):
    pass


class Martial(Weapon):
    name = "Martial"


class Simple(Weapon):
    name = "Simple"


class Armour(Equipment):
    pass


class Light(Armour):
    name = "Light"


class Medium(Armour):
    name = "Medium"


class Heavy(Armour):
    name = "Heavy"


class Shields(Armour):
    name = "Shields"

class Tools:
    pass

class Thieves(Tools):
    name = "Thieves' tools"

if __name__ == '__main__':
    pass
