from Character_Sheet.reference.items.items_key import Item, Weapon
from Character_Sheet.reference.items.jargon import *

Props = Weapon.PropertyKeys


class Simple(Weapon):
    name = "Simple"
    suffix = "Weapon"
    plural = 0


class Martial(Weapon):
    name = "Martial"
    suffix = "Weapon"
    plural = 0


class Improvised(Weapon):
    name = "Improvised"
    suffix = "Weapon"
    plural = 0


class Ranged(Weapon):
    name = "Ranged"
    suffix = "Weapon"
    plural = 0


class Melee(Weapon):
    name = "Melee"
    suffix = "Weapon"
    plural = 0


class Club(Simple, Melee):
    name = "Club"
    plural = 0
    cost = sp(1)
    dmg = (1, 4, b)
    weight = 2
    properties = Weapon.properties(Props.light)


class Dagger(Simple, Melee):
    name = "Dagger"
    plural = 0
    cost = gp(2)
    dmg = (1, 4, s)
    weight = 1
    properties = Weapon.properties(Props.finesse, Props.light, Props.thrown(20, 60))


class Greatclub(Simple, Melee):
    name = "Greatclub"
    plural = 0
    cost = gp(2)
    dmg = (1, 8, b)
    weight = 10
    properties = Weapon.properties(Props.two_handed)


class Handaxe(Simple, Melee):
    name = "Handaxe"
    plural = 0
    cost = gp(5)
    dmg = (1, 6, s)
    weight = 2
    properties = Weapon.properties(Props.light, Props.thrown(20, 60))


class Javelin(Simple, Melee):
    name = "Javelin"
    plural = 0
    cost = sp(5)
    dmg = (1, 6, p)
    weight = 2
    properties = Weapon.properties(Props.thrown(30, 120))


class LightHammer(Simple, Melee):
    name = "Light Hammer"
    plural = 0
    cost = gp(2)
    dmg = (1, 4, b)
    weight = 2
    properties = Weapon.properties(Props.light, Props.thrown(20, 60))


class Mace(Simple, Melee):
    name = "Mace"
    plural = 0
    cost = gp(5)
    dmg = (1, 6, b)
    weight = 4
    properties = Weapon.properties()


class Quarterstaff(Simple, Melee):
    name = "Quarterstaff"
    plural = 0
    cost = sp(2)
    dmg = (1, 6, b)
    weight = 4
    properties = Weapon.properties(Props.versatile(1, 8))


class Sickle(Simple, Melee):
    name = "Sickle"
    plural = 0
    cost = gp(1)
    dmg = (1, 4, s)
    weight = 2
    properties = Weapon.properties(Props.light)


class Spear(Simple, Melee):
    name = "Spear"
    plural = 0
    cost = gp(1)
    dmg = (1, 6, p)
    weight = 3
    properties = Weapon.properties(Props.thrown(20, 60), Props.versatile(1, 8))


class LightCrossbow(Simple, Ranged):
    name = "Light Crossbow"
    plural = 0
    cost = gp(25)
    dmg = (1, 8, p)
    weight = 5
    properties = Weapon.properties(Props.ammunition(80, 320), Props.loading, Props.two_handed)


class Dart(Simple, Ranged):
    name = "Dart"
    plural = 0
    cost = cp(5)
    dmg = (1, 4, p)
    weight = 0.25
    properties = Weapon.properties(Props.finesse, Props.thrown(20, 60))


class Shortbow(Simple, Ranged):
    name = "Shortbow"
    plural = 0
    cost = gp(25)
    dmg = (1, 6, p)
    weight = 2
    properties = Weapon.properties(Props.ammunition(80, 320), Props.two_handed)


class Sling(Simple, Ranged):
    name = "Sling"
    plural = 0
    cost = sp(1)
    dmg = (1, 4, b)
    weight = 0
    properties = Weapon.properties(Props.ammunition(30, 120))


class Battleaxe(Martial, Melee):
    name = "Battleaxe"
    plural = 0
    cost = gp(10)
    dmg = (1, 8, s)
    weight = 4
    properties = Weapon.properties(Props.versatile(1, 10))


class Flail(Martial, Melee):
    name = "Flail"
    plural = 0
    cost = gp(10)
    dmg = (1, 8, p)
    weight = 2
    properties = Weapon.properties()


class Glaive(Martial, Melee):
    name = "Glaive"
    plural = 0
    cost = gp(20)
    dmg = (1, 10, s)
    weight = 6
    properties = Weapon.properties(Props.heavy, Props.reach, Props.two_handed)


class Greataxe(Martial, Melee):
    name = "Greataxe"
    plural = 0
    cost = gp(30)
    dmg = (1, 12, s)
    weight = 7
    properties = Weapon.properties(Props.heavy, Props.two_handed)


class Greatsword(Martial, Melee):
    name = "Greatsword"
    plural = 0
    cost = gp(50)
    dmg = (2, 6, s)
    weight = 6
    properties = Weapon.properties(Props.heavy, Props.two_handed)


class Halberd(Martial, Melee):
    name = "Halberd"
    plural = 0
    cost = gp(20)
    dmg = (1, 10, s)
    weight = 6
    properties = Weapon.properties(Props.heavy, Props.reach, Props.two_handed)


class Lance(Martial, Melee):
    name = "Lance"
    plural = 0
    cost = gp(10)
    dmg = (1, 12, p)
    weight = 6
    properties = Weapon.properties(Props.reach, Props.special("You have disadvantage when you use a lance to Attack a "
                                                              "target within 5 feet of you. Also, a lance requires "
                                                              "two hands to wield when you aren't mounted."))


class Longsword(Martial, Melee):
    name = "Longsword"
    plural = 0
    cost = gp(15)
    dmg = (1, 8, s)
    weight = 3
    properties = Weapon.properties(Props.versatile(1, 10))


class Maul(Martial, Melee):
    name = "Maul"
    plural = 0
    cost = gp(10)
    dmg = (2, 6, b)
    weight = 10
    properties = Weapon.properties(Props.heavy, Props.two_handed)


class Morningstar(Martial, Melee):
    name = "Morningstar"
    plural = 0
    cost = gp(15)
    dmg = (1, 8, p)
    weight = 4
    properties = Weapon.properties()


class Pike(Martial, Melee):
    name = "Pike"
    plural = 0
    cost = gp(5)
    dmg = (1, 10, p)
    weight = 18
    properties = Weapon.properties(Props.heavy, Props.reach, Props.two_handed)


class Rapier(Martial, Melee):
    name = "Rapier"
    plural = 0
    cost = gp(25)
    dmg = (1, 8, p)
    weight = 2
    properties = Weapon.properties(Props.finesse)


class Scimitar(Martial, Melee):
    name = "Scimitar"
    plural = 0
    cost = gp(25)
    dmg = (1, 6, s)
    weight = 3
    properties = Weapon.properties(Props.finesse, Props.light)


class Shortsword(Martial, Melee):
    name = "Shortsword"
    plural = 0
    cost = gp(10)
    dmg = (1, 6, p)
    weight = 2
    properties = Weapon.properties(Props.finesse, Props.light)


class Trident(Martial, Melee):
    name = "Trident"
    plural = 0
    cost = gp(5)
    dmg = (1, 6, p)
    weight = 4
    properties = Weapon.properties(Props.thrown(20,60), Props.versatile(1, 8))


class WarPick(Martial, Melee):
    name = "War Pick"
    plural = 0
    cost = gp(5)
    dmg = (1, 8, p)
    weight = 2
    properties = Weapon.properties()



class Warhammer(Martial, Melee):
    name = "Warhammer"
    plural = 0
    cost = gp(15)
    dmg = (1, 8, b)
    weight = 2
    properties = Weapon.properties(Props.versatile(1, 10))


class Whip(Martial, Melee):
    name = "Whip"
    plural = 0
    cost = gp(2)
    dmg = (1, 4, s)
    weight = 3
    properties = Weapon.properties(Props.finesse, Props.reach)



class Blowgun(Martial, Ranged):
    name = "Blowgun"
    plural = 0
    cost = gp(10)
    dmg = (1, p)
    weight = 1
    properties = Weapon.properties(Props.ammunition(25,100), Props.loading)



class HandCrossbow(Martial, Ranged):
    name = "Hand Crossbow"
    plural = 0
    cost = gp(75)
    dmg = (1, 6, p)
    weight = 3
    properties = Weapon.properties(Props.ammunition(30,120), Props.light, Props.loading)



class HeavyCrossbow(Martial, Ranged):
    name = "Heavy Crossbow"
    plural = 0
    cost = gp(50)
    dmg = (1, 10, p)
    weight = 18
    properties = Weapon.properties(Props.ammunition(100, 400), Props.heavy, Props.loading, Props.two_handed)



class Longbow(Martial, Ranged):
    name = "Longbow"
    plural = 0
    cost = gp(50)
    dmg = (1, 8, p)
    weight = 2
    properties = Weapon.properties(Props.ammunition(150, 600), Props.heavy, Props.two_handed)

class Net(Martial, Ranged):
    name = "Net"
    plural = 0
    cost = gp(1)
    dmg = None
    weight = 3
    properties = Weapon.properties(Props.special("A Large or smaller creature hit by a net is Restrained until it is "
                                                 "freed. A net has no Effect on creatures that are formless, "
                                                 "or creatures that are Huge or larger. A creature can use its action "
                                                 "to make a DC 10 Strength check, freeing itself or another creature "
                                                 "within its reach on a success. Dealing 5 slashing damage to the net "
                                                 "(AC 10) also frees the creature without harming it, Ending the "
                                                 "Effect and destroying the net. When you use an action, "
                                                 "Bonus Action, or Reaction to Attack with a net, you can make only "
                                                 "one Attack regardless of the number of attacks you can normally "
                                                 "make."), Props.thrown(5, 15))