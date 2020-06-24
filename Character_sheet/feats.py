from helper_classes import *
import helper_functions as f

class Feat:
        def __init__(self, name, desc, prereq, effects):
                self.name = name
                self.desc = desc
                self.prereq = prereq
                self.effects = effects

feats = {}

feats["actor"] = Feat("Actor", "Skilled at mimicry and dramatics, you gain the following benefits:", 
        False,
        [Modifier("attributes.CHA", +1), 
        Note("skills.deception", "Advantage when pretending to be someone else."), 
        Note("skills.performance", "Advantage when pretending to be someone else."),
        Feature("role_play", "You can mimic the speech of another person or the sounds made by other creatures. You must have heard the person speaking, or heard the creature make the sound, for at least 1 minute. A successful Wisdom (Insight) check contested by your Charisma (Deception) check allows a listener to determine that the effect is faked.")])

feats["heavily_armored"] = Feat("Heavily Armoured", "You have trained to master the use of heavy armor, gaining the following benefits:", 
        ["armor", "Medium"], 
        [Modifier("attributes.STR", +1), 
        Modifier("profficiencies.armor", "Heavy")])

feats["shield_master"] = Feat("Shield Master", "You use shields not just for protection but also for offense. You gain the following benefits while you are wielding a shield:",
        False,
        [Feature("actions.bonus", "If you take the Attack action on your turn, you can use a bonus action to try to shove a creature within 5 feet of you with your shield."),
        Note("saving_throws.DEX", "Add shield's AC bonus if only you are targeted by spell or harmful effect, and if not incapacitated."),
        Note("saving_throws.DEX", "You can use your reaction to take no damage, if successful on a saving throw to take half damage from an effect.")])

# add_feat(feats_obj, "race", "heavily_armored")