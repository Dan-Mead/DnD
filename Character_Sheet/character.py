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
from flatten_dict import flatten, unflatten

import Character_Sheet.helpers as helpers
import Character_Sheet.reference.glossary as glossary
import Character_Sheet.reference.races as races
import Character_Sheet.reference.classes as classes
import Character_Sheet.reference.items as items
import Character_Sheet.reference.backgrounds as backgrounds
import Character_Sheet.reference.skills_and_attributes as skills


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

            # Size and Speed
            self.data["stats"]["size"] = {"base": race_instance.size,
                                          "temp": {}}
            self.data["stats"]["speed"] = {"base": race_instance.speed,
                                           "temp": {}}

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

        self.init_data()

        base_file = "Ser Gorden Simpleton.pkl"
        # base_file = "Kargal the Wretched.pkl"
        self.load_base_char(base_file)

    def init_data(self):

        self.data = {}

        info_keys = ["name",
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

        self.data["info"] = dict.fromkeys(info_keys)

        skill_dict = glossary.skills_dict
        all_attrs = glossary.attrs

        self.data["stats"] = {"size": {"base": "",
                                       "current": "",
                                       "temp": None},
                              "speed": {"base": "",
                                        "current": "",
                                        "temp": None,
                                        "mods": {}},
                              "level": None,
                              "prof": None}

        self.data["ability scores"] = {attr: {"base": None, "mods": {}, "override": {}} for attr in all_attrs}
        self.data["saving throws"] = {attr: {"prof": [], "mods": {}, "override": {},
                                             "notes": {}, "adv": {}, "disadv": {}} for attr in all_attrs}
        self.data["skills"] = {skill.replace("_", " "): {"prof": [], "expertise": [], "mods": {}, "override": {},
                                                         "notes": {}, "adv": {}, "disadv": {},
                                                         "attr": values[1]} for skill, values in skill_dict.items()}

        self.data["class"] = {"starting class": None,
                              "classes": {}}

        weapon_list = set(helpers.list_end_values(items.Weapon))
        all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
        [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

        self.data["proficiencies"] = {
            "weapons": {"unarmed": [True], "simple": [], "martial": []} | {weapon.name: [] for weapon in
                                                                           weapon_list},
            "armour": {"light": [], "medium": [], "heavy": [], "shields": []},
            "languages": {language: [] for language in glossary.all_languages},
            "tools": {tool.name.lower().replace("_", " "): [] for tool in all_tools}}

        flavour_keys = ["background",
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

        self.data["flavour"] = dict.fromkeys(flavour_keys)

        self.data["HP"] = {"current": math.nan,
                           "max": 0,
                           "temp": 0,
                           "death_saves": False,
                           "death_saves_passed": [0 for i in range(3)],
                           "death_saves_failed": [0 for i in range(3)]}

        self.data["health"] = {"AC": {"current": 10,
                                      "base": 10,
                                      "modifiers": []},
                               "defences": {},
                               "immunities": {},
                               "conditions": {}}

        self.data["inventory"] = {"currency": {"gp": 0,
                                               "sp": 0,
                                               "cp": 0},
                                  "all": [],
                                  "wieldable": {},
                                  "wearable": {},
                                  "other": {},
                                  "equipped": {"armour": None}}

        # TODO: Categorise inventory

        self.data["feats"] = {}

        self.data["features"] = {}

        self.data["features_list"] = {}

    def change_value(self, path, value):
        temp_dict = flatten(self.data, keep_empty_types=(dict, list, tuple))
        temp_dict[path] = value
        self.data = unflatten(temp_dict)


if __name__ == "__main__":
    window = tk.Tk()
    character = Character()
    pass
