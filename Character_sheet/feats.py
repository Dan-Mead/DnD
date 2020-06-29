from helper_classes import *

class Feat:
        def __init__(self, name, desc, prereq, effects):
                self.name = name
                self.desc = desc
                self.prereq = prereq
                self.effects = effects

        ### Add method to add / remove features

def get_feats_list():
        feats_list = {"actor" : ['Actor', Actor, False],
                        "heavily_armored" : ['Heavily Armored', Heavily_Armored, ["armor", "Medium"]],
                        "shield_master" : ['Shield Master', Shield_Master, False]}

        return feats_list

def get_valid_feats(char):

        feats_list = get_feats_list()

        valid_feats = []

        for feat in feats_list:
                prereq = feats_list[feat][2]
                if prereq == False:
                        valid_feats.append(feat)
                elif prereq[0] == 'armor':
                        groups = char.profficiencies.armor.values()
                        armors = [armor for group in groups for armor in group]
                        if prereq[1] in armors:
                                valid_feats.append(feat)

        return valid_feats

class Actor(Feat):
        def __init__(self):
                self.name = "Actor"
                self.desc = "Skilled at mimicry and dramatics, you gain the following benefits:"
                self.effects = [Modifier("attributes.CHA.feat", +1), 
                                Note("skills.deception.note.feat", "Advantage when pretending to be someone else."), 
                                Note("skills.performance.note.feat", "Advantage when pretending to be someone else."),
                                Feature("role_play.feat", "You can mimic the speech of another person or the sounds made by other creatures. You must have heard the person speaking, or heard the creature make the sound, for at least 1 minute. A successful Wisdom (Insight) check contested by your Charisma (Deception) check allows a listener to determine that the effect is faked.")]

class Heavily_Armored(Feat):
        def __init__(self):
                self.name = "Heavily Armored"
                self.desc = "You have trained to master the use of heavy armor, gaining the following benefits:"
                self.effect = [Modifier("attributes.STR.feat", +1),
                               Modifier("profficiencies.armor.feat", "Heavy")]

class Shield_Master(Feat):
        def __init__(self): 
                self.name = "Shield Master"
                self.desc = "You use shields not just for protection but also for offense. You gain the following benefits while you are wielding a shield:",
                self.prereq = False
                self.effects = [Feature("actions.bonus.feat", "If you take the Attack action on your turn, you can use a bonus action to try to shove a creature within 5 feet of you with your shield."),
                                Note("saving_throws.DEX.note.feat", "Add shield's AC bonus if only you are targeted by spell or harmful effect, and if not incapacitated."),
                                Note("saving_throws.DEX.note.feat", "You can use your reaction to take no damage, if successful on a saving throw to take half damage from an effect.")]