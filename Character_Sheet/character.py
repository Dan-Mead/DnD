import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

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


def import_info(filename):
    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()
    return info

class SimpleValue:
    def __init__(self):
        self.variable = tk.StringVar()

    def __repr__(self):
        return repr(self.get())

    def update(self):
        pass

    def set(self, text):
        self.variable.set(text)

    def get(self):
        return self.variable.get()


class CompositeValues:
    class Alignment(SimpleValue):
        def __init__(self, ethic_target, morality_target):
            super().__init__()
            self.ethics = ethic_target
            self.morality = morality_target

        def update(self):
            text = F"{self.ethics.get()} {self.morality.get()}"
            self.set(text)

    class Race(SimpleValue):
        def __init__(self, race_target, subrace_target):
            super().__init__()
            self.race = race_target
            self.subrace = subrace_target

        def update(self):
            race_name = self.race.get()
            subrace_name = self.subrace.get()

            race_val = {race.race_name: race for race in races.Race.__subclasses__()}[race_name]
            subrace_opts = [subrace.subrace_name for subrace in race_val.__subclasses__()]

            if subrace_opts and subrace_name in subrace_opts:
                subrace_string = f" ({subrace_name})"
            else:
                subrace_string = ""

            text = F"{race_name}{subrace_string}"
            self.set(text)


class ComplexValues:
    class Size(SimpleValue):
        def __init__(self, race_name):
            super().__init__()
            self.race_name = race_name
            self.size = None
            self.override = None

        def update(self):
            if not self.override:
                self.set(races.race_list[self.race_name.get()].size)

    class Speed(SimpleValue):
        def __init__(self, race_name):
            super().__init__()
            self.race_name = race_name
            self.override = {"base": [],
                             "temp": []}

        def update(self):
            if not any(self.override.values()):
                self.set(races.race_list[self.race_name.get()].speed)
            else:
                if self.override["temp"]:
                    self.set(max(self.override["temp"]))
                else:
                    self.set(max(self.override["base"]))

class All:
    named_items = {}
    for item in helpers.list_end_values(items.Item):
        if hasattr(item, "name"):
            named_items[item.name] = item

class Character:
    def __init__(self):
        self.imported = {}



        self.updatables = []

        self.race_config()
        self.class_config()
        self.info_config()
        self.profs_config()
        self.ability_scores_config()
        self.skills_config()
        self.flavour_config()
        self.feats_config()
        self.features_config()
        self.defences_config()
        self.inventory_config()
        self.other_config()

    def info_config(self):

        self.info = {}

        simple_values = ["name",
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
                         "morality"]

        for value in simple_values:
            self.info[value] = SimpleValue()

        self.info["alignment"] = CompositeValues.Alignment(self.info["ethics"], self.info["morality"])
        self.info["race_print"] = CompositeValues.Race(self.race["name"], self.race["subrace"])

        self.info["size"] = ComplexValues.Size(self.race["name"])
        self.info["speed"] = ComplexValues.Speed(self.race["name"])

        self.updatables.append(self.info["alignment"])
        self.updatables.append(self.info["race_print"])
        self.updatables.append(self.info["size"])
        self.updatables.append(self.info["speed"])

    def race_config(self):

        self.race = {"name": tk.StringVar(),
                     "subrace": tk.StringVar()}

    def class_config(self):

        self.class_ = {"starting class": tk.StringVar()}

    def profs_config(self):

        all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
        [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

        self.proficiencies = {"Languages": {lang: False for lang in glossary.all_languages},
                              "Armour": {armour.name: False for armour in
                                         [items.Light, items.Medium, items.Heavy, items.Shields]},
                              "Weapons": {weapon.name: False for weapon in items.Simple.__subclasses__() +
                                          items.Martial.__subclasses__()},
                              "Tools": {tool.name: False for tool in all_tools}
                              }

    def ability_scores_config(self):

        class AbilityScore:
            def __init__(self, name):
                self.attr = name
                self.base = 0
                self.race = 0
                self.feat = 0
                self.ASI = 0
                self.misc = 0
                self.override = None

                self.raw = tk.StringVar()
                self.mod = tk.StringVar()

                self.checkables = ["base", "race", "feat", "ASI", "misc"]

            def add_modifier(self, name, value=0):
                setattr(self, name, value)
                self.checkables.append(name)

            def update(self):
                if self.override:
                    print("Override not currently functional")
                else:
                    raw_val = sum([getattr(self, attribute) for attribute in self.checkables])

                    self.raw.set(raw_val)

                    mod_val = math.floor((raw_val - 10) / 2)

                    self.mod.set(F"{mod_val:+}")

                    self.raw_val = self.raw.get()
                    self.mod_val = self.mod.get()

        self.ability_scores = {attr: AbilityScore(attr) for attr in glossary.attrs}

        for score_object in self.ability_scores.values():
            self.updatables.append(score_object)

        self.saving_throws = {attr: {"prof": False,
                                     "notes": []} for attr in glossary.attrs}

        self.saving_throws["Notes"] = []

    def skills_config(self):

        self.skills = {skill.name: skill for skill in skills.Skill.__subclasses__()}

        for skill in self.skills.values():
            skill.prof = False
            skill.expertise = False

    def flavour_config(self):
        self.flavour = {"background": tk.StringVar(),
                        "background name": tk.StringVar(),
                        "background feature": tk.StringVar(),
                        "backstory": tk.StringVar(),
                        "traits": tk.StringVar(),
                        "ideals": tk.StringVar(),
                        "bonds": tk.StringVar(),
                        "flaws": tk.StringVar(),
                        "allies": tk.StringVar(),
                        "enemies": tk.StringVar(),
                        "organisations": tk.StringVar(),
                        "physical appearance": tk.StringVar(),
                        "other_affiliations": tk.StringVar(),
                        "other notes": tk.StringVar(),

                        }

    def feats_config(self):

        self.num_feats = 0
        self.feats = {}

    def features_config(self):

        self.features = {"All": {},
                         "Other": {}}

    def defences_config(self):
        self.defences = []
        self.immunities = []

    def inventory_config(self):

        self.inventory = {"items": [],
                          "currency": {"gp": 0,
                                       "sp": 0,
                                       "cp": 0}}

    def other_config(self):
        self.image_path = None

    def load(self):

        self.__init__()

        # filename = "C:/Users/Dan/OneDrive/Code/DnD/Character_Sheet/saves/Ser Gorden Simpleton.pkl"

        filename = tk.filedialog.askopenfilename(initialdir="saves/",
                                                 title="Select save file",
                                                 filetypes=(
                                                     ("Pickled Files", "*.pkl"),
                                                     ("all files", "*.*")))

        character_import_dict = import_info(filename)

        self.imported.update(character_import_dict)

        # for key, value in character_import_dict.items():
        #     print(key,": ", value)

        self.process_imported()

    def process_imported(self):

        # Import basic stuff

        checked_off = {key: False for key in self.imported.keys()}

        imported_destination_key = {"Name": self.info["name"],
                                    "Age": self.info["age"],
                                    "Gender": self.info["gender"],
                                    "Skin Colour": self.info["skin colour"],
                                    "Height": self.info["height"],
                                    "Weight": self.info["weight"],
                                    "Eye Colour": self.info["eye colour"],
                                    "Hair Colour": self.info["hair colour"],
                                    "Build": self.info["build"],
                                    "Faith": self.info["faith"],
                                    "Ethics": self.info["ethics"],
                                    "Morality": self.info["morality"],
                                    "Race": self.race["name"],
                                    "Subrace": self.race["subrace"],
                                    "Background": self.flavour["background"],
                                    "Background Name": self.flavour["background name"],
                                    "Background Feature": self.flavour["background feature"],
                                    "Backstory": self.flavour["backstory"],
                                    "Traits": self.flavour["traits"],
                                    "Ideals": self.flavour["ideals"],
                                    "Bonds": self.flavour["bonds"],
                                    "Flaws": self.flavour["flaws"],
                                    "Allies": self.flavour["allies"],
                                    "Enemies": self.flavour["enemies"],
                                    "Organisations": self.flavour["organisations"],
                                    "Physical Appearance": self.flavour["physical appearance"],
                                    "Other_affiliations": self.flavour["other_affiliations"],
                                    "Other Notes": self.flavour["other notes"],
                                    "Class": self.class_["starting class"],
                                    }

        for origin, destination in imported_destination_key.items():
            try:
                origin_value = self.imported[origin]
                checked_off[origin] = True
                destination.set(origin_value)
            except KeyError:
                pass

        for key, value in self.imported.items():
            try:
                # Ability Scores
                if "ASI" in key:
                    if "Final Choice" in key:
                        attr = key[-3:]
                        if not value:
                            value = 10
                        self.ability_scores[attr].base = int(value)
                        checked_off[key] = True

                #     if "Race ASI" in key:
                #         self.ability_scores[value].race += 1
                #         checked_off[key] = True
                #
                # # Languages
                # elif "Language" in key:
                #     if value != "None":
                #         self.proficiencies["Languages"][value] = True
                #     checked_off[key] = True
                #
                # # Tools
                #
                # elif any([skill in key for skill in ["Tool", "tool", "Tools", "tools"]]):
                #     if value != "None":
                #         self.proficiencies["Tools"][value] = True
                #     checked_off[key] = True
                #
                # # Skills
                #
                # elif any([skill in key for skill in ["Skill", "skill", "Skills", "skills"]]):
                #     self.skills[value].prof = True
                #     checked_off[key] = True
                #
                # Other

                elif key == "Character Image Path":
                    self.image_path = value
                    checked_off[key] = True
            except KeyError:
                print(F"{key} has no value")

        self.scrape_rcb()

        # print("\nUnused values:")
        # for value, checked in checked_off.items():
        #     if not checked:
        #         print(value)

        self.update_all()

    def scrape_rcb(self):

        # ASI, Skills, Languages, Tools

        def race_scrape():

            def get_instances():
                race_name = self.race["name"].get()

                if races.race_list[race_name].__subclasses__():
                    subrace_name = self.race["subrace"].get()
                else:
                    subrace_name = ""

                race_instance = races.race_list[race_name]
                if subrace_name:
                    subrace_instance = {subrace.subrace_name: subrace for subrace in race_instance.__subclasses__()}[
                        subrace_name]
                else:
                    subrace_instance = None

                return race_instance, subrace_instance

            def ASI():

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
                        self.ability_scores[attr].race += val

            def languages():

                for lang in race_instance.languages:  # assume only race has languages, may be untrue
                    if isinstance(lang, str):
                        self.proficiencies["Languages"][lang] = True
                    else:
                        for key, value in self.imported.items():
                            if "language" in key.lower() and "race" in key.lower():
                                self.proficiencies["Languages"][value] = True

            def other_features():
                all_features = {}
                if race_instance.features:
                    all_features.update(race_instance.features.all)
                if subrace_instance and subrace_instance.features and subrace_instance.features != race_instance.features:
                    all_features.update(subrace_instance.features.all)

                def feature_switcher(feature_name, feature_type, feature_val):
                    if feature_type == races.FeatureType.skills:

                        if isinstance(feature_val, (list, tuple)):
                            for key, value in self.imported.items():
                                if "skill" in key.lower() and feature_name in key:
                                    self.skills[value].prof = True

                        else:
                            print("Adjust skill scrape for ", feature_name)

                    elif feature_type == races.FeatureType.proficiencies:

                        if isinstance(feature_val, (list, tuple)):
                            for key, value in self.imported.items():
                                if "tool" in key.lower() and feature_name in key:
                                    # print(key, value)
                                    self.proficiencies["Tools"][value] = True
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

                                # self.proficiencies["Tools"][value] = True

                    # Other, feats, choice
                    elif feature_type == races.FeatureType.feats:
                        self.num_feats += 1

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

            race_instance, subrace_instance = get_instances()
            ASI()
            languages()
            other_features()

        def class_scrape():

            class_name = self.class_["starting class"].get()
            class_instance = classes.class_list[class_name]

            self.hit_die = class_instance.hit_die
            self.lvl_up_hp = class_instance.lvl_up_hp

            for armour in class_instance.armour_proficiencies:
                self.proficiencies["Armour"][armour.name] = True

            for prof in class_instance.weapon_proficiencies:
                for weapon in prof.__subclasses__():
                    self.proficiencies["Weapons"][weapon.name] = True

            for tool in class_instance.tool_proficiencies:
                self.proficiencies["Tools"][tool.name] = True

            for save in class_instance.saving_throws:
                self.saving_throws[save.__name__]["prof"] = True

            for key, value in self.imported.items():
                if "skill" in key.lower() and "class" in key.lower():
                    if value:
                        self.skills[value].prof = True

                elif "equipment" in key.lower() and "class" in key.lower():

                    selections = value["selected"]
                    choices = value["chosen"]
                    chosen_num = 0

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
                                                    self.inventory["items"].append(item(num))
                                            chosen_num += 1
                                        else:
                                            self.inventory["items"].append(item)
                                else:
                                    for item in selected:
                                        if isinstance(item, tuple):
                                            chosen_num += 1
                                        elif item.__class__.__subclasses__():
                                            chosen_num += 1
                        else:
                            item = selection[0]
                            self.inventory["items"].append(item)

            # print(self.imported["equipment"])

            # for skill_name, skill in self.skills.items():
            #     print(skill_name, skill.prof)

        def bg_scrape():

            background_name = self.flavour["background"].get()

            try:
                background_instance = backgrounds.background_list[background_name]
            except KeyError:
                background_instance = None


        race_scrape()
        class_scrape()
        bg_scrape()

    def update_all(self):
        for object in self.updatables:
            object.update()

if __name__ == "__main__":
    window = tk.Tk()
    char = Character()
    char.load()

    for item in char.inventory["items"]:
        print(item.syntax().capitalize())

    # print(char.features["Other"])
