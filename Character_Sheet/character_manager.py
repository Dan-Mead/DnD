import tkinter as tk
from tkinter import ttk

from Character_Sheet.character import Character

from Character_Sheet.reference.items import *
import Character_Sheet.helpers as helpers
import Character_Sheet.reference.skills_and_attributes as skills
import Character_Sheet.reference.glossary as glossary


class Aspect:
    def __init__(self):
        self.update()

        if self.type == str:
            self.tkVar = tk.StringVar()
        elif self.type == int:
            self.tkVar = tk.IntVar()
        elif self.type == bool:
            self.tkVar = tk.BooleanVar()

        self.pull()

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
            self.pull()
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
                                 width = 20,
                                 justify=tk.CENTER)
                entry.insert(tk.END, self.get_value(source_path))
                entry.pack()
                # edit_window.mainloop()

                cancel_button = tk.Button(edit_window, width = 8, text = "Cancel", command = cancel)
                save_button = tk.Button(edit_window, width = 8, text = "Save", command = save)

                cancel_button.pack()
                save_button.pack()

    def update(self):
        pass

################### Actual Aspects ###################

class Name(Aspect):
    source = {"Name": ("info", "name")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()


class Race(Aspect):
    source = {"Race": ("info", "race"),
              "Subrace": ("info", "subrace")}
    type = str
    protected = True

    def __init__(self):
        super().__init__()

    def pull(self):
        race_name = self.get_value(self.source["Race"])
        subrace_name = self.get_value(self.source["Subrace"])

        value = f"{race_name} ({subrace_name})"
        self.set(value)

class Level(Aspect):
    source = {"Level": ("stats", "level")}
    type = int
    protected = True

    def __init__(self):
        super().__init__()

    def update(self):
        char.data["stats"]["level"] = sum([lvl for lvl in char.data["class"]["classes"].values()])

class Alignment(Aspect):
    source = {"Ethics": ("info", "ethics"),
              "Morality": ("info", "morality")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

    def pull(self):
        ethics = self.get_value(self.source["Ethics"])
        morality = self.get_value(self.source["Morality"])

        value = f"{ethics} {morality}"
        self.set(value)

class Size(Aspect):
    source = {"Size": ("stats", "size", "current")}
    type = str
    protected = True

    def __init__(self):
        super().__init__()

    def update(self):

        if not char.data["stats"]["size"]["temp"]:
            char.data["stats"]["size"]["current"] = char.data["stats"]["size"]["base"]
        else:
            char.data["stats"]["size"]["current"] = char.data["stats"]["size"]["temp"]

class Speed(Aspect):
    source = {"Speed": ("stats", "speed", "current")}
    type = str
    protected = True

    def __init__(self):
        super().__init__()

    def pull(self):
        value = self.get_value(self.source["Speed"])
        value = f"{value} ft."
        self.set(value)

    def update(self):

        if not char.data["stats"]["speed"]["temp"]:
            char.data["stats"]["speed"]["current"] = char.data["stats"]["speed"]["base"]
        else:
            char.data["stats"]["speed"]["current"] = char.data["stats"]["speed"]["temp"]

class Faith(Aspect):
    source = {"Faith": ("info", "faith")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

class Skin(Aspect):
    source = {"Skin Colour": ("info", "skin colour")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

class Eyes(Aspect):
    source = {"Eye Colour": ("info", "eye colour")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

class Hair(Aspect):
    source = {"Faith": ("info", "hair colour")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()


class Height(Aspect):
    source = {"Faith": ("info", "height")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()


class Weight(Aspect):
    source = {"Faith": ("info", "weight")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()


class Build(Aspect):
    source = {"Faith": ("info", "build")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

class Age(Aspect):
    source = {"Faith": ("info", "age")}
    type = int
    protected = False

    def __init__(self):
        super().__init__()

class Gender(Aspect):
    source = {"Faith": ("info", "gender")}
    type = str
    protected = False

    def __init__(self):
        super().__init__()

class Aspects:

    aspects = {
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
    }

    def __init__(self):
        self.add_all()

    def add_all(self):
        for aspect, object in self.aspects.items():
            setattr(self, aspect, object())

    def update_all(self):
        for aspect, object in self.aspects.items():
            getattr(self, aspect).update()

char = Character()

if __name__ == "__main__":
    window = tk.Tk()
    Aspects()

    # CM.name.edit()

    # window.mainloop()

    pass





# class CharacterManager:
#     """Converts a character data format into tkinter variables for use by
#     the character sheet. Should eventually work both ways, allowing editing of values."""
#
#     class DisplayValue:
#
#         def __init__(self):
#             self.add_display_value()
#
#         def add_display_value(self):
#             self.disp = tk.StringVar()
#             self.disp.set(self.val)
#
#         def get(self):
#             pass
#
#         def set(self):
#             pass
#
#     class SingleSourceValue(DisplayValue):
#         def __init__(self, char):
#             self.val = helpers.list_as_keys(char.data, self.source)
#             super().__init__()
#
#     ### Actual Aspects
#     """Updatable defines if something is a base value or not, hence if it can
#     be updated or set without worrying about breaking something.
#     Source points to the relevant location(s) in the character data dictionary"""
#
#     class Name(SingleSourceValue):
#         updatable = True
#         source = ["info", "name"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Race(DisplayValue):
#         updatable = False
#         source = (["info", "race"],
#                   ["info", "subrace"])
#
#         def __init__(self, char):
#             values = []
#             for source in self.source:
#                 values.append(helpers.list_as_keys(char.data, source))
#             values[-1] = f"({values[-1]})"
#             self.val = " ".join(values)
#             super().__init__()
#
#     class Level(SingleSourceValue):
#         updatable = False
#         source = ["stats", "level"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Alignment(DisplayValue):
#         updatable = True
#         source = (["info", "ethics"],
#                   ["info", "morality"])
#
#         def __init__(self, char):
#             values = []
#             for source in self.source:
#                 values.append(helpers.list_as_keys(char.data, source))
#             self.val = " ".join(values)
#             super().__init__()
#
#     class Size(SingleSourceValue):
#         updatable = False
#         source = ["stats", "size", "current"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Speed(SingleSourceValue):
#         updatable = False
#         source = ["stats", "speed", "current"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Faith(SingleSourceValue):
#         updatable = True
#         source = ["info", "faith"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Skin(SingleSourceValue):
#         updatable = True
#         source = ["info", "skin colour"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Hair(SingleSourceValue):
#         updatable = True
#         source = ["info", "hair colour"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Eyes(SingleSourceValue):
#         updatable = True
#         source = ["info", "eye colour"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Height(SingleSourceValue):
#         updatable = True
#         source = ["info", "height"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Weight(SingleSourceValue):
#         updatable = True
#         source = ["info", "weight"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Build(SingleSourceValue):
#         updatable = True
#         source = ["info", "build"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Age(SingleSourceValue):
#         updatable = True
#         source = ["info", "age"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     class Gender(SingleSourceValue):
#         updatable = True
#         source = ["info", "gender"]
#
#         def __init__(self, char):
#             super().__init__(char)
#
#     aspects = {"name": Name,
#                "race": Race,
#                "level": Level,
#                "alignment": Alignment,
#                "size": Size,
#                "speed": Speed,
#                "faith": Faith,
#                "skin": Skin,
#                "hair": Hair,
#                "eyes": Eyes,
#                "height": Height,
#                "weight": Weight,
#                "build": Build,
#                "age": Age,
#                "gender": Gender,
#                }
#
#     class Attr:
#         source = ["ability scores"]
#
#         def __init__(self, attr, char):
#             pass
#
#     # Should probably make this better at just being automatically updated
#
#     def __init__(self, char):
#
#         self.char = char
#
#         for aspect, object in self.aspects.items():
#             setattr(self, aspect, object(char))
#
#         for attr in glossary.attrs:
#             setattr(self, attr, self.Attr(attr, char))
#
#         # for aspect in self.aspects.keys():
#         #     # try:
#         #     getattr(self, aspect).disp.get()
#         # except AttributeError:
#         #     print(F"{aspect.capitalize()} not fully implemented in converter.")
#
#         # pass
