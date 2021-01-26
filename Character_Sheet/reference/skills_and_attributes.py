class Skill:
    pass


class Attribute:
    pass


class STR(Attribute):
    name = "Strength"



class DEX(Attribute):
    name = "Dexterity"


class CON(Attribute):
    name = "Constitution"


class INT(Attribute):
    name = "Intelligence"


class WIS(Attribute):
    name = "Wisdom"


class CHA(Attribute):
    name = "Charisma"


class Acrobatics(Skill):
    name = "Acrobatics"
    attr = DEX


class AnimalHandling(Skill):
    name = "Animal Handling"
    attr = WIS


class Arcana(Skill):
    name = "Arcana"
    attr = INT


class Athletics(Skill):
    name = "Athletics"
    attr = STR


class Deception(Skill):
    name = "Deception"
    attr = CHA


class History(Skill):
    name = "History"
    attr = INT


class Insight(Skill):
    name = "Insight"
    attr = WIS


class Intimidation(Skill):
    name = "Intimidation"
    attr = CHA


class Investigation(Skill):
    name = "Investigation"
    attr = INT


class Medicine(Skill):
    name = "Medicine"
    attr = WIS


class Nature(Skill):
    name = "Nature"
    attr = INT


class Perception(Skill):
    name = "Perception"
    attr = WIS


class Performance(Skill):
    name = "Performance"
    attr = CHA


class Persuasion(Skill):
    name = "Persuasion"
    attr = CHA


class Religion(Skill):
    name = "Religion"
    attr = INT


class SleightOfHand(Skill):
    name = "Sleight of Hand"
    attr = DEX


class Stealth(Skill):
    name = "Stealth"
    attr = DEX


class Survival(Skill):
    name = "Survival"
    attr = WIS


skills_list = {skill.name: skill for skill in Skill.__subclasses__()}
attr_list = {attr.__name__: attr for attr in Attribute.__subclasses__()}
