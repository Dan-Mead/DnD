from Character_Sheet.reference.skills_and_attributes import *
from Character_Sheet.reference.equipment import *


class Background():
    pass


class KnighlyOrder(Background):
    name = 'Knightly Order'
    skills = (Persuasion, "choose")
    skill_choices = (Arcana, History, Nature, Religion)
    tools = ([GamingSet, Instrument])
    languages = "Any"
    equipment = (TravellersClothes, Custom_Misc("Placeholder: Seal of Office",
                                                "A signet, banner, or seal representing your place or rank in the order"))
    currency = ((10, "g"),)
    feature = "You receive shelter and succor from members of your knightly order and those who are sympathetic to " \
              "its aims. If your order is a religious one, you can gain aid from temples and other religious " \
              "communities of your deity. Knights of civic orders can get help from the community—whether a lone " \
              "settlement or a great nation—that they serve, and knights of philosophical orders can find help from " \
              "those they have aided in pursuit of their ideals, and those who share their ideals." \
              "\n\n" \
              "This help comes in the form of shelter and meals, and healing when appropriate, as well as " \
              "occasionally risky assistance,  such as a band of local citizens rallying to aid a sorely pressed " \
              "knight, or those who support the order helping to smuggle a knight out of town when he or she is being " \
              "hunted unjustly. "


background_list = dict([(bg.name, bg) for bg in Background.__subclasses__()])
