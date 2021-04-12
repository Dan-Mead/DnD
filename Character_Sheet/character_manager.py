import tkinter as tk
from tkinter import ttk
import math

from Character_Sheet.character import Character

from Character_Sheet.reference.items import *
import Character_Sheet.helpers as helpers
import Character_Sheet.reference.skills_and_attributes as skills
import Character_Sheet.reference.classes as classes
import Character_Sheet.reference.glossary as glossary


class Aspect:
    def __init__(self, name):

        if name in Aspects.all:
            print(name, "repeated")

        Aspects.all[name] = self

        if self.type == str:
            self.tkVar = tk.StringVar()
        elif self.type == int:
            self.tkVar = tk.IntVar()
        elif self.type == bool:
            self.tkVar = tk.BooleanVar()

        self.update()

    def update(self):
        self.process()
        self.pull()
        return self

    def pull(self):
        source = list(self.source.values())[0]
        value = self.get_value(source)
        self.set(value)

    def get_value(self, source):
        return helpers.list_to_keys(char.data, source)

    def set(self, value):
        self.tkVar.set(value)
        self.disp = self.tkVar.get()

    def edit(self):

        def cancel():
            edit_window.destroy()

        def save():
            new_value = entry.get()
            char.change_value(source_path, new_value)
            self.update()
            edit_window.destroy()

        if self.protected == True:
            print(f"Aspect is protected!")
            pass

        else:
            for source_name, source_path in self.source.items():
                edit_window = tk.Tk()
                edit_label = tk.Label(edit_window, text=f"Editing value: {source_name}")
                edit_label.pack()
                entry = tk.Entry(edit_window,
                                 width=20,
                                 justify=tk.CENTER)
                entry.insert(tk.END, self.get_value(source_path))
                entry.pack()
                # edit_window.mainloop()

                cancel_button = tk.Button(edit_window, width=8, text="Cancel", command=cancel)
                save_button = tk.Button(edit_window, width=8, text="Save", command=save)

                cancel_button.pack()
                save_button.pack()

    def process(self):
        pass


################### Actual Aspects ###################

class Name(Aspect):
    source = {"Name": ("info", "name")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Race(Aspect):
    source = {"Race": ("info", "race"),
              "Subrace": ("info", "subrace")}
    type = str
    protected = True

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        race_name = self.get_value(self.source["Race"])
        subrace_name = self.get_value(self.source["Subrace"])

        value = f"{race_name} ({subrace_name})"
        self.set(value)


class Level(Aspect):
    source = {"Level": ("stats", "level")}
    type = int
    protected = True

    def __init__(self, name):
        super().__init__(name)

    def process(self):
        char.data["stats"]["level"] = sum([lvl for lvl in char.data["class"]["classes"].values()])


class Alignment(Aspect):
    source = {"Ethics": ("info", "ethics"),
              "Morality": ("info", "morality")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        ethics = self.get_value(self.source["Ethics"])
        morality = self.get_value(self.source["Morality"])

        value = f"{ethics} {morality}"
        self.set(value)


class Size(Aspect):
    source = {"Size": ("stats", "size", "current")}
    type = str
    protected = True

    def __init__(self, name):
        super().__init__(name)

    def process(self):

        if not char.data["stats"]["size"]["temp"]:
            char.data["stats"]["size"]["current"] = char.data["stats"]["size"]["base"]
        else:
            char.data["stats"]["size"]["current"] = char.data["stats"]["size"]["temp"]


class Speed(Aspect):
    source = {"Speed": ("stats", "speed", "current")}
    type = str
    protected = True

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        value = self.get_value(self.source["Speed"])
        value = f"{value} ft."
        self.set(value)

    def process(self):

        if not char.data["stats"]["speed"]["temp"]:
            char.data["stats"]["speed"]["current"] = char.data["stats"]["speed"]["base"]
        else:
            char.data["stats"]["speed"]["current"] = char.data["stats"]["speed"]["temp"]


class Faith(Aspect):
    source = {"Faith": ("info", "faith")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Skin(Aspect):
    source = {"Skin Colour": ("info", "skin colour")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Eyes(Aspect):
    source = {"Eye Colour": ("info", "eye colour")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Hair(Aspect):
    source = {"Faith": ("info", "hair colour")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Height(Aspect):
    source = {"Faith": ("info", "height")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Weight(Aspect):
    source = {"Faith": ("info", "weight")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Build(Aspect):
    source = {"Faith": ("info", "build")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Age(Aspect):
    source = {"Faith": ("info", "age")}
    type = int
    protected = False

    def __init__(self, name):
        super().__init__(name)


class Gender(Aspect):
    source = {"Faith": ("info", "gender")}
    type = str
    protected = False

    def __init__(self, name):
        super().__init__(name)


class AbilityRaw(Aspect):
    type = int
    protected = True

    def __init__(self, name, attr):
        self.attr = attr
        self.source = {f"{attr} Raw": ("ability scores", attr, "raw")}
        super().__init__(name)

    def process(self):

        # Ability Scores
        values = char.data["ability scores"][self.attr]

        if not values["override"]:
            values["raw"] = int(values["base"])
            for mod in values["mods"].values():
                values["raw"] += mod

        elif values["override"]:
            values["total"] = values["override"]


class AbilityMod(Aspect):
    type = str
    protected = True

    def __init__(self, name, attr):
        self.attr = attr
        self.source = {f"{attr} Mod": ("ability scores", attr, "mod")}
        super().__init__(name)

    def pull(self):
        source = list(self.source.values())[0]
        value = self.get_value(source)
        self.val = value
        self.set(F"{value:+}")

    def process(self):
        getattr(Aspects, self.attr)["raw"].update()
        values = char.data["ability scores"][self.attr]
        values["mod"] = math.floor((values["raw"] - 10) / 2)


class ProficiencyBonus(Aspect):
    type = int
    protected = True
    source = {"Level": ("stats", "prof")}

    def __init__(self, name):
        super().__init__(name)

    def process(self):
        Aspects.level.update()
        level = char.data["stats"]["level"]
        prof_bonus = math.floor(level / 4) + 2
        char.data["stats"]["prof"] = prof_bonus


class SavingThrowProf(Aspect):
    type = bool
    protected = True

    def __init__(self, name, attr):
        self.attr = attr
        self.source = {f"{attr} Save Prof": ("saving throws", attr, "prof")}
        super().__init__(name)

    def pull(self):
        source = list(self.source.values())[0]
        value = self.get_value(source)

        if value:
            self.set(True)
        else:
            self.set(False)


class SavingThrowVal(Aspect):
    type = str
    protected = True

    def __init__(self, name, attr):
        self.attr = attr
        self.source = {f"{attr} Save Val": ("saving throws", attr, "mod")}
        super().__init__(name)

    def pull(self):
        source = list(self.source.values())[0]
        value = self.get_value(source)
        self.val = value
        self.set(F"{value:+}")

    def process(self):
        getattr(Aspects, self.attr)["mod"].update()
        getattr(Aspects, self.attr)["save prof"].update()
        Aspects.proficiency_bonus.update()

        override = char.data["saving throws"][self.attr]["override"]
        if not override:
            profs = char.data["saving throws"][self.attr]["prof"]
            mods = char.data["saving throws"][self.attr]["mods"]

            output_val = char.data["ability scores"][self.attr]["mod"]

            if profs:
                output_val += char.data["stats"]["prof"]
            if mods:
                for origin, mod_val in mods:
                    output_val += mod_val

        else:
            output_val = override

        char.data["saving throws"][self.attr]["mod"] = output_val


class SkillProf(Aspect):
    type = bool
    protected = True

    def __init__(self, name, skill):
        self.skill = skill
        self.source = {f"{skill} Prof": ("skills", skill, "prof"),
                       f"{skill} Expertise": ("skills", skill, "expertise")}
        super().__init__(name)

    def pull(self):
        profs = self.get_value(self.source[f"{self.skill} Prof"])
        expertise = self.get_value(self.source[f"{self.skill} Expertise"])

        if profs:
            self.type = "proficient"
            if expertise:
                self.type = "expertise"

        # Else jack of all trades etc here.
        if profs or expertise:
            self.set(True)
        else:
            self.set(False)


class SkillVal(Aspect):
    type = str
    protected = True

    def __init__(self, name, skill):
        self.skill = skill
        self.source = {f"{skill} Val": ("skills", skill, "mod")}
        super().__init__(name)

    def pull(self):

        value = self.get_value(list(self.source.values())[0])
        self.val = value
        self.set(F"{value:+}")

    def process(self):
        attr = char.data["skills"][self.skill]["attr"]
        Aspects.proficiency_bonus.update()
        getattr(Aspects, attr)["mod"].update()

        prof_aspect = getattr(Aspects, self.skill)["prof"]
        prof_aspect.update()

        mod_val = char.data["ability scores"][attr]["mod"]

        if prof_aspect.type == "proficient":
            mod_val += char.data["stats"]["prof"]
        elif prof_aspect.type == "expertise":
            mod_val += 2 * char.data["stats"]["prof"]
        # Else jack of all trades etc.

        char.data["skills"][self.skill]["mod"] = mod_val


class PassiveWis(Aspect):
    type = int
    protected = True
    source = {"Wisdom Mod": ("ability scores", "WIS", "mod")}

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        value = self.get_value(list(self.source.values())[0])
        self.set(10 + value)

    def process(self):
        Aspects.WIS["mod"].update()


class PassiveInt(Aspect):
    type = int
    protected = True
    source = {"Intelligence Mod": ("ability scores", "INT", "mod")}

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        value = self.get_value(list(self.source.values())[0])
        self.set(10 + value)

    def process(self):
        Aspects.INT["mod"].update()


class MaxHP(Aspect):
    type = int
    protected = True
    source = {"Max HP": ("HP", "max")}

    def __init__(self, name):
        super().__init__(name)

    def process(self):

        starting_class = char.data["class"]["starting class"]
        class_instance = classes.class_list[starting_class]

        max_hp = 0
        max_hp += class_instance.hit_die

        for class_name, lvl in char.data["class"]["classes"].items():
            class_instance = classes.class_list[class_name]
            if class_name == char.data["class"]["starting class"]:
                lvl -= 1
            max_hp += lvl * class_instance.lvl_up_hp

        max_hp += char.data["stats"]["level"] * char.data["ability scores"]["CON"]["mod"]
        char.data["HP"]["max"] = max_hp


class CurrentHP(Aspect):
    type = int
    protected = False,
    source = {"Current HP": ("HP", "current")}

    def __init__(self, name):
        super().__init__(name)

    def pull(self):
        source = list(self.source.values())[0]
        value = self.get_value(source)
        if math.isnan(value):
            value = self.get_value(("HP", "max"))
        self.set(value)


    def change_value(self, new_value):
        source_path = self.source["Current HP"]
        char.change_value(source_path, new_value)
        self.update()


class TempHP(Aspect):
    type = int
    protected = False,
    source = {"Temp HP": ("HP", "temp")}

    def __init__(self, name):
        super().__init__(name)

    def change_value(self, new_value):
        source_path = self.source["Temp HP"]
        char.change_value(source_path, new_value)
        self.update()


class DeathSave(Aspect):
    type = bool
    protected = False

    def __init__(self, name, p_f, i):
        self.index = i
        self.pass_fail = p_f
        self.source = {"Death Save": ("HP", f"death_saves_{p_f}")}
        super().__init__(name)

    def pull(self):
        saves = self.get_value(self.source["Death Save"])
        value = saves[self.index]
        self.set(value)


class Aspects:
    all = {}

    raw_aspects = {
        "name": Name,
        "race": Race,
        "level": Level,
        "alignment": Alignment,
        "size": Size,
        "speed": Speed,
        "faith": Faith,
        "skin": Skin,
        "hair": Hair,
        "eyes": Eyes,
        "height": Height,
        "weight": Weight,
        "build": Build,
        "age": Age,
        "gender": Gender,
        "proficiency_bonus": ProficiencyBonus,
        "temp_HP": TempHP
    }

    ability_dependent_aspects = {
        "passive_perception": PassiveWis,
        "passive_investigation": PassiveInt,
        "passive_insight": PassiveWis,
        "max_HP": MaxHP,
        "current_HP": CurrentHP,

    }

    # grouped_aspects = [([attr for attr in glossary.attrs], [""]

    def __init__(self):
        self.add_all()

    @classmethod
    def add_all(cls):
        for aspect, object in cls.raw_aspects.items():
            setattr(cls, aspect, object(aspect))

        for attr in glossary.attrs:
            setattr(cls, attr, {})
            getattr(cls, attr)["raw"] = AbilityRaw(f"{attr} raw", attr)
            getattr(cls, attr)["mod"] = AbilityMod(f"{attr} mod", attr)
            getattr(cls, attr)["save prof"] = SavingThrowProf(f"{attr} save prof", attr)
            getattr(cls, attr)["save val"] = SavingThrowVal(f"{attr} save val", attr)

        for skill in char.data["skills"].keys():
            setattr(cls, skill, {})
            getattr(cls, skill)["prof"] = SkillProf(f"{skill} prof", skill)
            getattr(cls, skill)["val"] = SkillVal(f"{skill} val", skill)

        for aspect, object in cls.ability_dependent_aspects.items():
            setattr(cls, aspect, object(aspect))

        setattr(cls, "death_saves", {})

        for p_f in ["passed", "failed"]:
            getattr(cls, "death_saves")[p_f] = {}
            for i in range(3):
                getattr(cls, "death_saves")[p_f][i] = DeathSave(f"death_saves_{p_f}_{i}", p_f, i)


    @classmethod
    def update_all(cls):

        char.data["class"]["classes"]["Paladin"] = 2

        for aspect, object in cls.all.items():
            object.update()


char = Character()

if __name__ == "__main__":
    window = tk.Tk()
    Aspects().update_all()

    # CM.name.edit()

    # window.mainloop()

    pass
