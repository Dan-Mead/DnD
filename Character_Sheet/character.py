import os
import pickle
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


def import_info(filename):

    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()
    return info


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


### Helper Functions and Items

class Updatable:
    values = []

    @classmethod
    def update_all(cls, char):
        for object in cls.values:
            object.update(char)


class ExportDict:
    values = {}

    @classmethod
    def export(cls):
        dict = {}
        for key, item in cls.values.items():
            dict[key] = item.get()
        return dict

    def import_data(cls):
        pass


class My:

    @staticmethod
    def StringVar(save_key=None):
        value = tk.StringVar()
        if save_key:
            ExportDict.values[save_key] = value
        return value

    @staticmethod
    def BooleanVar(save_key=None):
        value = tk.BooleanVar()
        if save_key:
            ExportDict.values[save_key] = value
        return value

    @staticmethod
    def IntVar(save_key=None):
        value = tk.IntVar()
        if save_key:
            ExportDict.values[save_key] = value
        return value


class SimpleValue:
    def __init__(self):
        self.textvariable = My.StringVar()

    # def __repr__(self):
    #     return repr(self.get())

    def set(self, text):
        self.textvariable.set(text)

    def get(self):
        return self.textvariable.get()


class CompositeValues:
    class Alignment(SimpleValue):
        def __init__(self, ethic_target, morality_target):
            super().__init__()
            Updatable.values.append(self)
            self.ethics = ethic_target
            self.morality = morality_target

        def update(self, char):
            text = F"{self.ethics.get()} {self.morality.get()}"
            self.set(text)

    class Race(SimpleValue):
        def __init__(self, race_target, subrace_target):
            super().__init__()
            Updatable.values.append(self)
            self.race = race_target
            self.subrace = subrace_target

        def update(self, char):
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

    class ListValsString:
        def __init__(self, origin_list, min_height):
            self.list_vals = origin_list
            self.string = My.StringVar()
            self.min_height = min_height
            Updatable.values.append(self)

        def update(self, *_):
            vals = []
            for vals_set in self.list_vals:
                vals.extend([val for val in vals_set])
            string = "\n".join(vals)
            string += "\n" * (max((self.min_height - string.count("\n")), 0))

            self.string.set(string)


class ComplexValues:
    class Size(SimpleValue):
        def __init__(self, race_name):
            super().__init__()
            Updatable.values.append(self)
            self.race_name = race_name
            self.size = None
            self.override = None

        def update(self, *_):
            if not self.override:
                self.set(races.race_list[self.race_name.get()].size)

    class Speed(SimpleValue):
        def __init__(self, race_name):
            super().__init__()
            Updatable.values.append(self)
            self.race_name = race_name
            self.override = {"base": [],
                             "temp": []}

        def update(self, *_):
            if not any(self.override.values()):
                value = races.race_list[self.race_name.get()].speed
            else:
                if self.override["temp"]:
                    value = max(self.override["temp"])
                else:
                    value = max(self.override["base"])

            self.set(str(value) + " ft.")

    class ProficiencyBonus(SimpleValue):
        def __init__(self):
            super().__init__()
            Updatable.values.append(self)
            self.mod = My.StringVar()

        def update(self, char):
            char.level.update(char)
            mod = math.floor(char.level.get() / 4) + 2
            self.mod.set(F"{mod:+}")

    class Level(SimpleValue):
        def __init__(self):
            super().__init__()
            Updatable.values.append(self)
            self.level = My.IntVar()

        def update(self, char):
            val = 0
            for class_name, lvl in char.classes.items():
                val += lvl
            self.level.set(val)

        def set(self, val):
            self.level.set(val)

        def get(self):
            return self.level.get()

    class HP:
        def __init__(self):
            Updatable.values.append(self)
            self.max_hp = My.IntVar("max_hp")
            self.current_hp = My.IntVar("current_hp")
            self.temp_hp = My.IntVar("temp_hp")

        def update(self, char):
            char.ability_scores["CON"].update()
            con_mod = char.ability_scores["CON"].mod.get()
            if con_mod:
                con_mod = int(con_mod)
            else:
                con_mod = 0

            max_hp = classes.class_list[char.starting_class.get()].hit_die - \
                     classes.class_list[char.starting_class.get()].lvl_up_hp

            max_hp += char.level.get() * con_mod

            for class_name, lvl in char.classes.items():
                max_hp += lvl * classes.class_list[class_name].lvl_up_hp

            self.max_hp.set(max_hp)

    class AC:
        unarmoured = "unarmoured"
        armoured = "armoured"
        other = "other"

        def __init__(self):
            Updatable.values.append(self)
            self.val = My.IntVar()
            self.state = self.unarmoured
            self.shield = False

        def update(self, char):

            inventory = {item.name: item for item in char.inventory["items"]}

            try:
                worn = inventory[char.inventory["worn"].get()]
                self.state = self.armoured
            except KeyError:
                self.state = self.unarmoured

            dex_mod = char.ability_scores["DEX"].mod.get()
            if self.state == self.unarmoured:
                new_val = 10 + int(dex_mod)
            elif self.state == self.armoured:
                if isinstance(worn, items.Light):
                    new_val = worn.AC + int(dex_mod)
                elif isinstance(worn, items.Medium):
                    dex_mod = min(2, dex_mod)
                    new_val = worn.AC + int(dex_mod)
                elif isinstance(worn, items.Heavy):
                    new_val = worn.AC

            # Check for shields
            self.shield = False
            wielded_names = [name.get() for name in char.inventory["wielded"].values()]
            for wielded in wielded_names:
                if wielded in inventory.keys():
                    wielded_item = inventory[wielded]
                    if isinstance(wielded_item, items.Shields):
                        self.shield = True
            if self.shield:
                new_val += 2

            self.val.set(new_val)


class DeathSavingThrows:
    def __init__(self):
        self.passes = []
        self.fails = []
        for i in range(3):
            self.passes += [My.BooleanVar(F"death_save_pass_{i}")]
            self.fails += [My.BooleanVar(F"death_save_fail_{i}")]


### GLossary List

class All:
    named_items = {}
    for item in helpers.list_end_values(items.Item):
        if hasattr(item, "name"):
            named_items[item.name] = item


### Actual Object

class Character:
    def __init__(self):
        self.imported = {}

        # self.updatables = []

        self.race_config()
        self.class_config()
        self.info_config()
        self.profs_config()
        self.HP_config()
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

        # self.updatables.append(self.info["alignment"])
        # self.updatables.append(self.info["race_print"])
        # self.updatables.append(self.info["size"])
        # self.updatables.append(self.info["speed"])

    def race_config(self):

        self.race = {"name": My.StringVar("race_name"),
                     "subrace": My.StringVar("subrace_name")}

    def class_config(self):

        self.starting_class = My.StringVar("starting_class")

        self.classes = {}

        self.level = ComplexValues.Level()

        self.prof_bonus = ComplexValues.ProficiencyBonus()

    def HP_config(self):

        self.HP = ComplexValues.HP()

        self.death_saves = DeathSavingThrows()

    def profs_config(self):

        all_tools = [tool for tool in items.Tool.__subclasses__() if not tool.__subclasses__()]
        [all_tools.extend(tool.__subclasses__()) for tool in items.Tool.__subclasses__() if tool.__subclasses__()]

        self.proficiencies = {"Languages": {lang: My.BooleanVar() for lang in glossary.all_languages},
                              "Armour": {armour.name: My.BooleanVar() for armour in
                                         [items.Light, items.Medium, items.Heavy, items.Shields]},
                              "Weapons": {weapon.name: My.BooleanVar() for weapon in items.Simple.__subclasses__() +
                                          items.Martial.__subclasses__()},
                              "Tools": {tool.name: My.BooleanVar() for tool in all_tools},
                              "Major": []}

    def ability_scores_config(self):

        class AbilityScore:
            def __init__(self, name):
                Updatable.values.append(self)
                self.attr = name
                self.base = 0
                self.race = 0
                self.feat = 0
                self.ASI = 0
                self.misc = 0
                self.override = None

                self.raw = My.StringVar(F"ability_score_{self.attr}_raw")
                self.mod = My.StringVar(F"ability_score_{self.attr}_mod")

                self.checkables = ["base", "race", "feat", "ASI", "misc"]

            def add_modifier(self, name, value=0):
                setattr(self, name, value)
                self.checkables.append(name)

            def update(self, *_):

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

        # for score_object in self.ability_scores.values():
        #     self.updatables.append(score_object)

        class SavingThrow:
            def __init__(self, attr):
                Updatable.values.append(self)
                self.attr = attr
                # self.ability_mod = ability_score
                self.prof = My.BooleanVar(F"saving_throw_{self.attr}_prof")
                self.notes = []
                self.mod = My.StringVar()

            def update(self, char):

                val = 0
                char.ability_scores[self.attr].update(char)
                ability_score_mod = char.ability_scores[self.attr].mod
                # self.ability_scores[attr].mod

                val += int(ability_score_mod.get())

                char.prof_bonus.update(char)

                val += self.prof.get() * int(char.prof_bonus.mod.get())

                self.mod.set(F"{val:+}")

        self.saving_throws = {attr: SavingThrow(attr) for attr in glossary.attrs}

        # for saving_throw in self.saving_throws.values():
        #     self.updatables.append(saving_throw)

        self.saving_throws["Notes"] = []

    def skills_config(self):

        class Skill:
            def __init__(self, name, attr):
                Updatable.values.append(self)
                self.name = name
                self.prof = My.BooleanVar(F"skill_{self.name}_prof")
                self.expertise = My.BooleanVar(F"skill_{self.name}_expertise")
                self.attr = attr
                self.display = My.StringVar()

            def update(self, char):
                val = 0

                val += int(self.prof.get()) * int(char.prof_bonus.mod.get())
                val += int(char.ability_scores[self.attr.__name__].mod.get())

                self.mod = val
                self.display.set(F"{val:^+}")

                # mod

        self.skills = {skill.name: Skill(skill.name, skill.attr) for skill in skills.Skill.__subclasses__()}

        class PassiveSkills:

            class PassiveSkill:
                def __init__(self, name, skill):
                    self.name = name
                    self.skill = skill
                    self.mod = My.StringVar()

                def update(self):
                    mod = self.skill.mod + 10
                    self.mod.set(F"{mod}")

            def __init__(self, skill_list):
                Updatable.values.append(self)
                self.updatables = []
                for skill in skill_list:
                    setattr(self, skill.name.lower(), self.PassiveSkill(skill.name, skill))
                    self.updatables.append(getattr(self, skill.name.lower()))

            def update(self, *_):
                for skill in self.updatables:
                    skill.update()

        passives = ["Perception", "Investigation", "Insight"]
        passives = [self.skills[skill] for skill in passives]

        self.skills["passives"] = PassiveSkills(passives)

    def flavour_config(self):
        self.flavour = {"background": My.StringVar("background"),
                        "background name": My.StringVar("background name"),
                        "background feature": My.StringVar("background feature"),
                        "backstory": My.StringVar("backstory"),
                        "traits": My.StringVar("traits"),
                        "ideals": My.StringVar("ideals"),
                        "bonds": My.StringVar("bonds"),
                        "flaws": My.StringVar("flaws"),
                        "allies": My.StringVar("allies"),
                        "enemies": My.StringVar("enemies"),
                        "organisations": My.StringVar("organisations"),
                        "physical appearance": My.StringVar("physical appearance"),
                        "other_affiliations": My.StringVar("other_affiliations"),
                        "other notes": My.StringVar("other notes"),

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
        self.conditions = []

        self.AC = ComplexValues.AC()
        self.defence_string = CompositeValues.ListValsString([self.defences, self.immunities], 3)
        self.conditions_string = CompositeValues.ListValsString([self.conditions], 3)

    def inventory_config(self):

        self.inventory = {"items": [],
                          "currency": {"gp": My.IntVar("currency_gold"),
                                       "sp": My.IntVar("currency_silver"),
                                       "cp": My.IntVar("currency_copper")},
                          "wielded": {1: My.StringVar("wielded_1"),
                                      2: My.StringVar("wielded_2")},
                          "worn": My.StringVar("worn_1")}

    def other_config(self):
        self.image_path = None

    def save(self, loc):

        def open_dict(dict_to_open):

            for key, item in dict_to_open.items():
                if isinstance(item, dict):
                    open_dict(item)
                elif isinstance(item, forbidden_types):
                    pass  # should be already taken care of
                elif isinstance(item, list):
                    print(key, item)
                    character[key] = item
                else:
                    pass  # print(key, item)

        character = ExportDict.export()

        char_dict = self.__dict__

        forbidden_types = (tk.StringVar, tk.BooleanVar, tk.IntVar)

        open_dict(char_dict)

        print(character["items"])

        with open(loc + '.pkl', "wb") as file:
            pickle.dump(character["items"], file, pickle.HIGHEST_PROTOCOL)
        file.close()

    def load(self, filename, type):

        # self.__init__() # Errors may begin to pile up here

        current_directory = os.getcwd()

        # filename = current_directory + "/saves/base_characters/Ser Gorden Simpleton.pkl"

        # filename = tk.filedialog.askopenfilename(initialdir="saves/",
        #                                          title="Select save file",
        #                                          filetypes=(
        #                                              ("Pickled Files", "*.pkl"),
        #                                              ("all files", "*.*")))

        if type == "base_character":

            character_import_dict = import_info(filename)

            self.imported.update(character_import_dict)

            self.process_imported()

            print("Finished importing")

        elif type == "active_character":
            pass

            # print(import_info(filename))

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
                                    "Class": self.starting_class,
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

        Updatable.update_all(self)

        self.long_rest()

        # self.update_all()

    def scrape_rcb(self):

        # ASI, Skills, Languages, Tools

        imported_items = []

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
                        self.proficiencies["Languages"][lang].set(True)
                    else:
                        for key, value in self.imported.items():
                            if "language" in key.lower() and "race" in key.lower():
                                self.proficiencies["Languages"][value].set(True)

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
                                    self.skills[value].prof.set(True)

                        else:
                            print("Adjust skill scrape for ", feature_name)

                    elif feature_type == races.FeatureType.proficiencies:

                        if isinstance(feature_val, (list, tuple)):
                            for key, value in self.imported.items():
                                if "tool" in key.lower() and feature_name in key:
                                    # print(key, value)
                                    self.proficiencies["Tools"][value].set(True)
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

            class_name = self.starting_class.get()
            class_instance = classes.class_list[class_name]
            self.classes[class_name] = 1

            self.hit_die = class_instance.hit_die
            self.lvl_up_hp = class_instance.lvl_up_hp

            for armour in class_instance.armour_proficiencies:
                self.proficiencies["Major"].append(armour)
                self.proficiencies["Armour"][armour.name].set(True)

            for prof in class_instance.weapon_proficiencies:
                self.proficiencies["Major"].append(prof)
                for weapon in prof.__subclasses__():
                    self.proficiencies["Weapons"][weapon.name].set(True)

            for tool in class_instance.tool_proficiencies:
                self.proficiencies["Tools"][tool.name].set(True)

            for save in class_instance.saving_throws:
                self.saving_throws[save.__name__].prof.set(True)

            for key, value in self.imported.items():
                if "skill" in key.lower() and "class" in key.lower():
                    if value:
                        self.skills[value].prof.set(True)

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

        def bg_scrape():

            background_name = self.flavour["background"].get()

            try:
                background_instance = backgrounds.background_list[background_name]
            except KeyError:
                background_instance = None

            if background_instance:

                # Skills

                for skill in background_instance.skills:
                    if not isinstance(skill, tuple):
                        self.skills[skill.name].prof.set(True)
                    else:
                        for key, value in self.imported.items():
                            if "background" in key.lower() and "skill" in key.lower():
                                self.skills[value].prof.set(True)

                # Tools

                if background_instance.tools:
                    for tool in background_instance.tools:
                        if isinstance(tool, tuple) or tool.__subclasses__():
                            for key, value in self.imported.items():
                                if "background" in key.lower() and "tool" in key.lower():
                                    self.proficiencies["Tools"][value].set(True)
                        else:
                            self.proficiencies["Tools"][tool.name] = True

                # Languages

                if background_instance.languages:
                    for language in background_instance.languages:
                        if isinstance(language, (tuple, list)):
                            for key, value in self.imported.items():
                                if "background" in key.lower() and "language" in key.lower():
                                    if value.lower() != "none":
                                        self.proficiencies["Languages"][value].set(True)
                        else:
                            self.proficiencies["Languages"][language].set(True)

                # Equipment

                if background_instance.equipment:
                    for item in background_instance.equipment:
                        imported_items.append(item)

        race_scrape()
        class_scrape()
        bg_scrape()

        self.inventory["items"], currencies = unpack_items(imported_items)

        for key, value in currencies.items():
            current = self.inventory["currency"][key].get()
            new = current + value
            self.inventory["currency"][key].set(new)

    def update_all(self):
        Updatable.update_all(self)

    def long_rest(self):
        self.HP.update(self)
        max_hp = self.HP.max_hp.get()
        self.HP.current_hp.set(max_hp)

    def short_rest(self):
        pass


if __name__ == "__main__":
    window = tk.Tk()
    char = Character()
    # char.load()

    # for item in char.inventory["items"]:
    #     print(item.syntax().capitalize())
    # for name, skill in char.skills.items():
    #     print(name, skill.prof)
    # print(char.features["Other"])
