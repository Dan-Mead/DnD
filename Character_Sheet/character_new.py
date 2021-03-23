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

        imported = import_info(first_load)
        self.imported = {}
        self.imported_checklist = {}
        for key, val in imported.items():
            self.imported[key.lower().replace("_", " ")] = val
            self.imported_checklist[key.lower().replace("_", " ")] = False

        # helpers.simple_print_dict_sep(self.imported)

        for aspect_type, aspects in self.data.items():
            for aspect in aspects:
                if aspect in self.imported.keys():
                    self.data[aspect_type][aspect] = self.imported[aspect]
                    self.imported_checklist[aspect] = True
        self.data["class"]["starting class"] = self.imported["class"]
        self.imported_checklist["class"] = True

        # helpers.simple_print_dict(self.data)

        for key, checked in self.imported_checklist.items():
            if checked:
                print(key, "|", self.imported[key])

        print("*************************************8")

        for key, checked in self.imported_checklist.items():
            if not checked:
                print(key, "|", self.imported[key])

        def scrape_race():

            race_name = self.imported["race"]
            race_instance = races.race_list[race_name]

            if races.race_list[race_name].__subclasses__():
                subrace_name = self.imported["subrace"]
                subrace_instance = {subrace.subrace_name: subrace for subrace in race_instance.__subclasses__()}[
                    subrace_name]
            else:
                subrace_name = ""
                subrace_instance = None

            race_origin = f"Race: {race_name} {subrace_name}"

            # Get race ASI

            race_ASI = []

            if subrace_instance and hasattr(subrace_instance, "ASI"):
                all_ASI = list(subrace_instance.ASI)
                if hasattr(race_instance, "ASI") and race_instance.ASI != subrace_instance.ASI:
                    all_ASI.extend(race_instance.ASI)
            else:
                if hasattr(race_instance, "ASI"):
                    all_ASI = list(race_instance.ASI)

            for ASI in all_ASI:
                attr, val = ASI
                if isinstance(attr, (tuple, list)):
                    for key, value in self.imported.items():
                        key_factors = key.split(" ")
                        if "asi" in key_factors:
                            if "race" in key_factors or "subrace" in key_factors:
                                race_ASI.append((value, 1))
                                self.imported_checklist[key] = True
                else:
                    race_ASI.append((attr.__name__, val))

            for increase in race_ASI:
                attr, val = increase
                if attr:
                    self.data["ability_scores"][attr]["mods"].update({race_origin: val})

            # Get Race Languages

            for lang in race_instance.languages:  # assume only race has languages, may be untrue
                if isinstance(lang, str):
                    self.data["proficiencies"]["languages"][lang] = {True: race_origin}
                else:
                    for key, value in self.imported.items():
                        if "language" in key.lower() and "race" in key.lower():
                            self.proficiencies["Languages"][value].set(True)

        scrape_race()

        class_name = self.imported["class"]
        bg_name = self.imported["background"]



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
        self.FeatureList(self)

        base_file = "Ser Gorden Simpleton.pkl"
        base_file = "Kargal the Wretched.pkl"
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

            char.data["stats"] = {"size": {"base": ""},
                                  "speed": {"base": ""}}

            char.data["ability_scores"] = {attr: {"base": None, "mods": {}, "override": {}} for attr in all_attrs}
            char.data["saving throws"] = {attr: {"prof": False, "mods": {}, "override": {},
                                                 "notes": {}, "adv": {}, "disadv": {}} for attr in all_attrs}
            char.data["skills"] = {skill: {"prof": False, "mods": {}, "override": {},
                                           "notes": {}, "adv": {}, "disadv": {}} for skill in skill_dict}

    class CharClass:
        def __init__(self, char):
            char.data["class"] = {"starting class": None}

    class Profs:
        def __init__(self, char):
            weapon_list = set(helpers.list_end_values(items.Weapon))
            all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
            [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

            char.data["proficiencies"] = {
                "weapons": {"unarmed": True, "simple": False, "martial": False} | {weapon.name: False for weapon in
                                                                                   weapon_list},
                "armour": {"light": False, "medium": False, "heavy": False, "shields": False},
                "languages": {language: False for language in glossary.all_languages},
                "tools": {tool.name: False for tool in all_tools}}

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
                    "other affiliations",
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

    class FeatureList:
        def __init__(self, char):
            char.data["features_list"] = {}


if __name__ == "__main__":
    window = tk.Tk()
    character = Character()
