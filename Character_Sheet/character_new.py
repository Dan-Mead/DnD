import os
import pickle, pickle5
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path

from functools import partial
import textwrap
import num2words
import math

import Character_Sheet.helpers as helpers
import Character_Sheet.reference.glossary as glossary
import Character_Sheet.reference.races as races
import Character_Sheet.reference.classes as classes
import Character_Sheet.reference.items as items
import Character_Sheet.reference.backgrounds as backgrounds
import Character_Sheet.reference.skills_and_attributes as skills


# Anything that isn't needs its own save/load aspect. Really need to remember this. Probably best to get a save/load converter object.

# Objects which need to update should act on the dict.
# Values on the charactersheet should be custom tkinter values, which update the respective value in base data

def import_info(filename):
    file = open(filename, "rb")
    try:
        info = pickle.load(file)
    except ValueError:
        info = pickle5.load(file)
    file.close()
    return info


class Character:

    # class Updatable:
    #     values = []
    #
    #     @classmethod
    #     def update_all(cls):

    def load(self):
        pass

    def load_base_char(self, filename):

        base_repo = Path.cwd() / "saves" / "base_characters"

        # [d.name for d in base_repo.iterdir()]

        first_load = Path.joinpath(base_repo, filename)

        info = import_info(first_load)

        # for key, val in info.items():
        #     print(key, "|", val)

        info_checklist = {key.lower(): {"key": key,
                                        "checked": False} for key in info.keys()}

        for type_ in self.data:
            for aspect in self.data[type_]:
                if aspect in info_checklist.keys():
                    key = info_checklist[aspect]["key"]
                    self.data[type_][aspect] = info[key]
                    info_checklist[aspect]["checked"] = True


        # Get race, etc values here, to put in specficially.
        directors = [(["race", "language"], self.data["profs"]["languages"], bool, None),
                     (["race", "asi"], self.data["stats"]["abilities"], "mod", "race"),
                     (["class", "skill"], self.data["stats"]["skills"], "prof", "class")]

        for key, val in info_checklist.items():
            if val["checked"] == False:
                # print(key, "|", info[val["key"]])

                key_factors = key.split(" ")
                value = info[val["key"]]
                for factors, direction, d_type, values in directors:
                    if all(factor in key_factors for factor in factors):
                        if d_type == bool:
                            direction[value] = True
                            val["checked"] = True
                        if d_type == "mod":
                            direction[value]["mods"] = {values: 1}
                            val["checked"] = True
                        if d_type == "prof"

        # print(self.data["stats"]["abilities"])

        for key, val in info_checklist.items():
            if val["checked"] == False:
                print(key, "|", info[val["key"]])

    def save(self):
        pass

    def __init__(self):

        self.data = {}

        self.Info(self)
        self.Stats(self)
        self.Flavour(self)
        self.CharClass(self)
        self.Profs(self)
        self.HP(self)
        self.Inventory(self)
        self.Feats(self)
        self.Features(self)
        self.Defences(self)

        base_file = "Ser Gorden Simpleton.pkl"
        self.load_base_char(base_file)

    class Info:
        def __init__(self, char):
            keys = ["name",
                    "age",
                    "gender",
                    "skin colour",
                    "height",
                    "weight",
                    "hair colour",
                    "eye colour",
                    "build",
                    "faith",
                    "ethics",
                    "morality",
                    "race",
                    "subrace"
                    ]

            char.data["info"] = dict.fromkeys(keys)

    class Stats:
        def __init__(self, char):

            skill_dict = glossary.skills_dict
            all_attrs = glossary.attrs

            char.data["stats"] = {"abilities": {attr: {"base": None, "mods": {}, "override": {}} for attr in all_attrs},
                                  "saving throws": {attr: {"prof": False, "mods": {}, "override": {},
                                                           "notes": {}, "adv": {}, "disadv": {}} for attr in all_attrs},
                                  "skills": {skill: {"prof": False, "mods": {}, "override": {},
                                                     "notes": {}, "adv": {}, "disadv": {}} for skill in skill_dict}}

    class CharClass:
        def __init__(self, char):
            char.data["class"] = {"starting class": None}

    class Profs:
        def __init__(self, char):
            weapon_list = set(helpers.list_end_values(items.Weapon))
            all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
            [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

            char.data["profs"] = {
                "weapons": {"unarmed": True, "simple": False, "martial": False} | {weapon.name: False for weapon in
                                                                                   weapon_list},
                "armour": {"light": False, "medium": False, "heavy": False, "shields": False},
                "languages": {language: False for language in glossary.all_languages},
                "Tools": {tool.name: False for tool in all_tools}}

    class Flavour:
        def __init__(self, char):
            keys = ["background",
                    "background name",
                    "background feature",
                    "backstory",
                    "traits",
                    "ideals",
                    "bonds",
                    "flaws",
                    "allies",
                    "enemies",
                    "organisations",
                    "other_affiliations",
                    "physical appearance",
                    "other notes",
                    "character image path"]

            char.data["flavour"] = dict.fromkeys(keys)

    class HP:
        def __init__(self, char):
            char.data["HP"] = {"current": None,
                               "temp": None,
                               "death_saves": False,
                               "death_saves_passed": 0,
                               "death_saves_failed": 0}

    class Inventory:
        def __init__(self, char):
            char.data["inventory"] = {"currency": {"gold": 0,
                                                   "silver": 0,
                                                   "copper": 0},
                                      "wieldable": {},
                                      "armour": {},
                                      "other": {}}

    class Feats:
        def __init__(self, char):
            char.data["feats"] = {}

    class Features:
        def __init__(self, char):
            char.data["features"] = {}

    class Defences:
        def __init__(self, char):
            char.data["defences"] = {}


if __name__ == "__main__":
    window = tk.Tk()
    character = Character()
