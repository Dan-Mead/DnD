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

        self.imported = import_info(first_load)

        # for key, val in info.items():
        #     print(key, "|", val)

        info_checklist = {key.lower().replace("_", " "): {"key": key,
                                                          "checked": False}
                          for key in self.imported.keys()}

        # Load base info, items that have simple, basic correspondances.

        for type_ in self.data:
            for aspect in self.data[type_]:
                if aspect in info_checklist.keys() and isinstance(aspect, str):
                    key = info_checklist[aspect]["key"]
                    self.data[type_][aspect] = self.imported[key]
                    info_checklist[aspect]["checked"] = True
                else:
                    print(aspect)

        race_name = self.imported["Race"]

        if races.race_list[race_name].__subclasses__():
            subrace_name = self.imported["Subrace"]
        else:
            subrace_name = ""

        class_name = self.imported["Class"]
        bg_name = self.imported["Background"]

        # Get more complex values, generally require bespoke implementation which is bad but kinda unavoidable.
        # def old_version():
        #     classifiers = [(["race", "language"], "languages", bool, f"Race: {race_val}"),
        #                    (["race", "asi"], "abilities", "mod", f"Race: {race_val}"),
        #                    (["class", "skill"], "skills", "prof", f"Class: {class_val}"),
        #                    (["subrace", "skills"], "skills", "prof", f"Race: {race_val} ({subrace_val})"),
        #                    (["subrace", "skill"], "skills", "prof", f"Race: {race_val} ({subrace_val})"),
        #                    (["background", "skill"], "skills", "prof", f"Background: {bg_val}"),
        #                    (["background", "tool"], "tools", bool, f"Background: {bg_val}"),
        #                    (["background", "language"], "languages", bool, f"Background: {bg_val}")]
        #
        #     directors = {"languages": self.data["profs"]["languages"],
        #                  "abilities": self.data["stats"]["abilities"],
        #                  "skills": self.data["stats"]["skills"],
        #                  "tools": self.data["profs"]["tools"]}
        #
        #     self.data["features_list"].update({key: {} for key in directors.keys()})
        #
        #     for key, val in info_checklist.items():
        #         if val["checked"] == False:
        #             key_factors = key.split(" ")
        #             value = info[val["key"]]
        #             for factors, type, d_type, origins in classifiers:
        #                 if all(factor in key_factors for factor in factors):
        #                     if d_type == bool:
        #                         self.data["features_list"][type].setdefault(origins, []).append(value)
        #                         directors[type][value] = True
        #                         val["checked"] = True
        #                     elif d_type == "mod":
        #                         self.data["features_list"][type].setdefault(origins, []).append((value, "+1"))
        #                         directors[type][value]["mods"][origins] = 1
        #                         val["checked"] = True
        #                     if d_type == "prof":
        #                         self.data["features_list"][type].setdefault(origins, []).append(value)
        #                         directors[type][value.replace(" ", "_").lower()]["prof"] = True
        #                         val["checked"] = True
        #             if all([factor in key_factors for factor in ["asi", "final", "choice"]]):
        #                 attr = key_factors[-1].upper()
        #                 self.data["stats"]["abilities"][attr]["base"] = value
        #                 val["checked"] = True

        self.scrape_race(race_name, subrace_name)
        # self.scrape_class(class_name)
        # self.scrape_background(bg_name)

    def scrape_race(self, race_name, subrace_name):

        race_instance = races.race_list[race_name]

        if subrace_name:
            subrace_instance = {subrace.subrace_name: subrace for subrace in race_instance.__subclasses__()}[
                subrace_name]
        else:
            subrace_instance = None

        self.data["stats"]["size"]["base"] = race_instance.size
        self.data["stats"]["speed"]["base"] = race_instance.speed

        ## Scrape ASI values, comparatively complex
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
                    if "race" in key.lower() and "ASI" in key:
                        race_ASI.append((value, 1))
            else:
                race_ASI.append((attr.__name__, val))

        for increase in race_ASI:
            attr, val = increase
            if attr:
                self.data["abilities"][attr]["mods"]["race"] = val

        ## Scrape Language

        for language in race_instance.languages:
            if isinstance(language, str):
                self.data["profs"]["languages"][language] = True


    def scrape_class(self, class_name):


        class_instance = classes.class_list[class_name]

        # Add starting equipment

        # self.inventory["items"], currencies = unpack_items(imported_items)
        #
        # for key, value in currencies.items():
        #     current = self.inventory["currency"][key].get()
        #     new = current + value
        #     self.inventory["currency"][key].set(new)


    def scrape_background(self, bg_name):

        try:
            background_instance = backgrounds.background_list[bg_val]
        except KeyError:
            background_instance = None

        # Add background feature
        self.data["features"]["background"] = info["Background Feature"]
        info_checklist["background feature"]["checked"] = True

        # Scrape Race features
        ## Scrape size and speed


        # Scrape Class

        # Add starting class

        self.data["class"]["starting class"] = class_val
        info_checklist["class"]["checked"] = True



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
        # base_file = "Kargal the Wretched.pkl"
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

            char.data["abilities"] = {attr: {"base": None, "mods": {}, "override": {}} for attr in all_attrs}
            char.data["saving throws"] = {attr: {"prof": False, "mods": {}, "override": {},
                                                 "notes": {}, "adv": {}, "disadv": {}} for attr in all_attrs},
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

            char.data["profs"] = {
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
