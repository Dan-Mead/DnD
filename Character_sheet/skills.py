#TUrn this into a property or something

class skill:
    def __init__(self, name, attr):
        self.name = name
        self.attr = attr
        self.prof = False

acrobatics = skill("Acrobatics", "DEX")
animal_handling = skill("Animal Handling", "WIS")
arcana = skill("Arcana", "INT")
athletics = skill("Athletics", "STR")
deception = skill("Deception", "CHA")
history = skill("History", "INT")
insight = skill("Insight", "WIS")
intimidation = skill("Intimidation", "CHA")
investigation = skill("Investigation", "INT")
medicine = skill("Medicine", "WIS")
nature = skill("Nature", "INT")
perception = skill("Perception", "WIS")
performance = skill("Performance", "CHA")
persuasion = skill("Persuasion", "CHA")
religion = skill("Religion", "INT")
sleight_of_hand = skill("Sleight of Hand", "DEX")
stealth = skill("Stealth", "DEX")
survival = skill("Survival", "WIS")