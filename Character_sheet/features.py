class Feature():
    pass

## TODO: Add triggers and actual effects

class Darkvision(Feature):
    def __init__(self):
        self.desc = "You can see in dim light within 60 feet of you as if it were bright light, and in Darkness as if it were dim light. You can’t discern color in Darkness, only Shades of Gray."

class Relentless_Endurance(Feature):
    def __init__(self):
        self.desc = "When you are reduced to 0 Hit Points but not killed outright, you can drop to 1 hit point instead. You can’t use this feature again until you finish a Long Rest."
        self.trigger = ["Zero HP"] ### WIP
        self.limited = [1, "Long Rest"]

class Savage_Attacks(Feature):
    def __init__(self):
        self.desc = "When you score a critical hit with a melee weapon Attack, you can roll one of the weapon’s damage dice one additional time and add it to the extra damage of the critical hit."
        self.trigger = ["Critical Hit"] ### WIP


feature_list = {"Darkvision" : Darkvision,
                "Relentless Endurance" : Relentless_Endurance, 
                "Savage Attacks" : Savage_Attacks
                }