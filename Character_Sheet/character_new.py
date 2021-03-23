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

# File Management

def import_info(filename):
    file = open(filename, "rb")
    try:
        info = pickle.load(file)
    except ValueError:
        info = pickle5.load(file)
    file.close()
    return info


# Other Functions

def unpack_items(item_list):
    all_items = []
    currencies = {"gp": 0,
                  "sp": 0,
                  "cp": 0}

    for item in item_list:
        if hasattr(item, "contents"):
            for obj in item.contents:
                if isinstance(obj, items.Currency):
                    currencies[obj.type] += obj.num
                else:
                    all_items.append(obj)
        all_items.append(item)

    return all_items, currencies


# Glossary List

class All:
    named_items = {}
    for item in helpers.list_end_values(items.Item):
        if hasattr(item, "name"):
            named_items[item.name] = item


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

        imported_items = []

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
                            for key_factor in key_factors:
                                if "race" in key_factor:
                                    race_ASI.append((value, 1))
                                    self.imported_checklist[key] = True
                else:
                    race_ASI.append((attr.__name__, val))

            for increase in race_ASI:
                attr, val = increase
                if attr:
                    self.data["ability scores"][attr]["mods"].update({race_origin: val})

            # Get Race Languages

            for lang in race_instance.languages:  # assume only race has languages, may be untrue
                if isinstance(lang, str):
                    self.data["proficiencies"]["languages"][lang] = [race_origin]
                else:
                    for key, value in self.imported.items():
                        key_factors = key.split(" ")
                        if "language" in key_factors or "languages" in key_factors:
                            for key_factor in key_factors:
                                if "race" in key_factor:
                                    if value.lower() != "none":
                                        self.data["proficiencies"]["languages"][value].append(race_origin)
                                    self.imported_checklist[key] = True
            all_features = {}
            if race_instance.features:
                all_features.update(race_instance.features.all)
            if subrace_instance and subrace_instance.features and subrace_instance.features != race_instance.features:
                all_features.update(subrace_instance.features.all)

            def feature_switcher(feature_name, feature_type, feature_val):
                if feature_type == races.FeatureType.skills:
                    if isinstance(feature_val, (list, tuple)):
                        for key, value in self.imported.items():
                            if "skill" in key and feature_name.lower() in key:
                                skill_key = value.lower().replace("_", " ")
                                self.data["skills"][skill_key]["prof"].append(race_origin)
                                self.imported_checklist[key] = True

                    else:
                        print("Adjust skill scrape for ", feature_name)

                elif feature_type == races.FeatureType.proficiencies:

                    if isinstance(feature_val, (list, tuple)):
                        for key, value in self.imported.items():
                            if "tool" in key and feature_name.lower() in key:
                                tool_name = value.lower().replace("_", " ")
                                self.data["proficiencies"]["tools"][tool_name].append(race_origin)
                                self.imported_checklist[key] = True
                    else:
                        print("Adjust skill scrape for ", feature_name)

                elif feature_type == races.FeatureType.choice:
                    try:
                        choices = race_instance.choice_features
                    except:
                        choices = subrace_instance.choice_features
                    else:
                        try:
                            choices += subrace_instance.choice_features
                        except:
                            pass

                    for key, value in self.imported.items():
                        if feature_name in key and "choice_features" in key[-len("choice_features"):]:
                            # print(key, ":", value)
                            choice = choices[value]

                            if isinstance(choice, tuple):
                                choice_type = choice[0]
                                choice_val = choice[1]
                                feature_switcher(value, choice_type, choice_val)

                            else:
                                print(f"Issue with choice formatting, check {feature_name}")

                # Other, feats, choice
                elif feature_type == races.FeatureType.feats:
                    self.data["feats"].setdefault("num", 0)
                    self.data["feats"]["num"] += 1

                elif feature_type == races.FeatureType.other:
                    feature_val.add(self, feature_name)

                else:
                    print(f"Must add {feature_type} support such as {feature_name}")

            for feature_name, feature_vals in all_features.items():
                if isinstance(feature_vals, list):
                    for feature in feature_vals:
                        feature_type = feature[0]
                        feature_val = feature[1]
                        feature_switcher(feature_name, feature_type, feature_val)

                elif isinstance(feature_vals, tuple):
                    feature_type = feature_vals[0]
                    feature_val = feature_vals[1]
                    feature_switcher(feature_name, feature_type, feature_val)

        scrape_race()

        def scrape_class():

            class_name = self.imported["class"]
            class_instance = classes.class_list[class_name]
            class_origin = f"Class: {class_name}"

            self.data["class"]["classes"][class_name] = 1
            # Something about chosing subclasses?

            for armour in class_instance.armour_proficiencies:
                self.data["proficiencies"]["armour"][armour.name.lower()].append(class_origin)

            for prof in class_instance.weapon_proficiencies:
                self.data["proficiencies"]["weapons"][prof.name.lower()].append(class_origin)
                for weapon in prof.__subclasses__():
                    self.data["proficiencies"]["weapons"][weapon.name].append(class_origin)

            for tool in class_instance.tool_proficiencies:
                tool_name = tool.name.lower().replace("_", " ")
                self.data["proficiencies"]["tools"][tool_name].append(class_origin)

            for save in class_instance.saving_throws:
                self.data["saving throws"][save.__name__]["prof"].append(class_origin)

            # Import choice values
            for key, value in self.imported.items():
                if "skill" in key and "class" in key:
                    if value:
                        skill_name = value.lower().replace("_", " ")
                        self.data["skills"][skill_name]["prof"].append(class_origin)
                        self.imported_checklist[key] = True

                # Get equipment
                elif "equipment" in key and "class" in key:
                    selections = value["selected"]
                    choices = value["chosen"]
                    chosen_num = 0
                    self.imported_checklist[key] = True
                    for i, selection in enumerate(class_instance.equipment):
                        if len(selection) > 1:
                            for j, selected in enumerate(selection):
                                if j == selections[i]:
                                    for item in selected:
                                        if item.__class__.__subclasses__() or isinstance(item, tuple):
                                            choice = choices[chosen_num]
                                            if isinstance(item, tuple):
                                                num = item[1]
                                            else:
                                                num = item.num

                                            for c in choice:
                                                if c in All.named_items:
                                                    item = All.named_items[c]
                                                    imported_items.append(item(num))
                                            chosen_num += 1
                                        else:
                                            imported_items.append(item)
                                else:
                                    for item in selected:
                                        if isinstance(item, tuple):
                                            chosen_num += 1
                                        elif item.__class__.__subclasses__():
                                            chosen_num += 1
                        else:
                            item = selection[0]
                            imported_items.append(item)

        scrape_class()

        def scrape_background():

            background_name = self.imported["background"]
            bg_origin = F"Background: {background_name}"
            try:
                background_instance = backgrounds.background_list[background_name]
            except KeyError:
                background_instance = None

            if background_instance:

                # Skills
                for skill in background_instance.skills:
                    if not isinstance(skill, tuple):
                        skill_name = skill.name.lower().replace("_", " ")
                        self.data["skills"][skill_name]["prof"].append(bg_origin)
                    else:
                        for key, value in self.imported.items():
                            if "background" in key and "skill" in key:
                                skill_name = value.lower().replace("_", " ")
                                self.data["skills"][skill_name]["prof"].append(bg_origin)
                                self.imported_checklist[key] = True

                # Tools
                if background_instance.tools:
                    for tool in background_instance.tools:
                        if isinstance(tool, tuple) or tool.__subclasses__():
                            for key, value in self.imported.items():
                                if "background" in key and "tool" in key:
                                    tool_name = value.lower().replace("_", " ")
                                    self.data["proficiencies"]["tools"][tool_name].append(bg_origin)
                                    self.imported_checklist[key] = True
                        else:
                            tool_name = tool.name.lower().replace("_", " ")
                            self.data["proficiencies"]["tools"][tool_name].append(bg_origin)

                # Languages

                if background_instance.languages:
                    for language in background_instance.languages:
                        if isinstance(language, (tuple, list)):
                            for key, value in self.imported.items():
                                if "background" in key.lower() and "language" in key.lower():
                                    if value.lower() != "none":
                                        self.data["proficiencies"]["languages"][value].append(bg_origin)
                                    self.imported_checklist[key] = True

                        else:
                            self.data["proficiencies"]["languages"][language].append(bg_origin)

                # Equipment

                if background_instance.equipment:
                    for item in background_instance.equipment:
                        imported_items.append(item)

        scrape_background()

        all_items, currencies = unpack_items(imported_items)

        self.data["inventory"]["all"].extend(all_items)

        for key, value in currencies.items():
            self.data["inventory"]["currency"][key] += value

        for key, val in self.imported.items():
            if all([factor in key for factor in ["asi", "final", "choice"]]):
                attr = key.split(" ")[-1].upper()
                self.data["ability scores"][attr]["base"] = val
                self.imported_checklist[key] = True

        for key, checked in self.imported_checklist.items():
            if not checked:
                print("Un-implemented feature!")
                print(key, "|", self.imported[key])

    def save(self):
        pass

    def __init__(self):

        self.data = {}

        self.aspects = [
            self.Info,
            self.Stats,
            self.Flavour,
            self.CharClass,
            self.Profs,
            self.HP,
            self.Inventory,
            self.Feats,
            self.Features,
            self.Defences,
            self.FeatureList,
        ]

        for aspect in self.aspects:
            # Init all listed aspects
            aspect(self)

        base_file = "Ser Gorden Simpleton.pkl"
        # base_file = "Kargal the Wretched.pkl"
        self.load_base_char(base_file)

        self.update_all()

        pass

    def update_all(self):
        for aspect in self.aspects:
            if hasattr(aspect, "update"):
                aspect.update(self)

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

            char.data["ability scores"] = {attr: {"base": None, "mods": {}, "override": {}} for attr in all_attrs}
            char.data["saving throws"] = {attr: {"prof": [], "mods": {}, "override": {},
                                                 "notes": {}, "adv": {}, "disadv": {}} for attr in all_attrs}
            char.data["skills"] = {skill.replace("_", " "): {"prof": [], "expertise": [], "mods": {}, "override": {},
                                                             "notes": {}, "adv": {}, "disadv": {}} for skill in
                                   skill_dict}

        @staticmethod
        def update(char):
            for attr, values in char.data["ability scores"].items():
                if not values["override"]:
                    values["total"] = int(values["base"])
                    for mod in values["mods"].values():
                        values["total"] += mod

                elif values["override"]:
                    values["total"] = values["override"]

                values["mod_val"] = math.floor((values["total"] - 10) / 2)

    class CharClass:
        def __init__(self, char):
            char.data["class"] = {"starting class": None,
                                  "classes": {}}

    class Profs:
        def __init__(self, char):
            weapon_list = set(helpers.list_end_values(items.Weapon))
            all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
            [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

            char.data["proficiencies"] = {
                "weapons": {"unarmed": [True], "simple": [], "martial": []} | {weapon.name: [] for weapon in
                                                                               weapon_list},
                "armour": {"light": [], "medium": [], "heavy": [], "shields": []},
                "languages": {language: [] for language in glossary.all_languages},
                "tools": {tool.name.lower().replace("_", " "): [] for tool in all_tools}}

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
            char.data["HP"] = {"current": 0,
                               "max": 0,
                               "temp": 0,
                               "death_saves": False,
                               "death_saves_passed": 0,
                               "death_saves_failed": 0}

        @staticmethod
        def update(char):
            starting_class = char.data["class"]["starting class"]
            class_instance = classes.class_list[starting_class]

            char.data["HP"]["max"] = 0
            char.data["HP"]["max"] += class_instance.hit_die

    class Inventory:
        def __init__(self, char):
            char.data["inventory"] = {"currency": {"gp": 0,
                                                   "sp": 0,
                                                   "cp": 0},
                                      "all": [],
                                      "wieldable": {},
                                      "wearable": {},
                                      "other": {}}

            #TODO: Categorise inventory

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
