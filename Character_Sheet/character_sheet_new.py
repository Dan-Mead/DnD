import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
from sys import platform

from functools import partial
import textwrap
import num2words

from Character_Sheet.character_new import Character
from Character_Sheet.reference.items import *
import Character_Sheet.helpers as helpers
import Character_Sheet.reference.skills_and_attributes as skills
import Character_Sheet.reference.glossary as glossary

default_font = "Verdana"

class ValueTypes:
    text = "text"
    choice = "choice"

class Info_Value_Pair:
    """Create a [TBD] editable text field with a label, for string/text values such as name or alignment.
    These should not change often."""

    def __init__(self,
                 master_frame,
                 label_text,
                 value_type=ValueTypes.text,
                 text="",
                 source=None,
                 text_font_mod=None,
                 grid=None,
                 pack=None):

        self.frame = tk.Frame(master_frame)


        if value_type == ValueTypes.text:
            self.value = tk.Label(self.frame,
                                  font=default_font + " 10")

            if text_font_mod:
                self.value.config(font=default_font + text_font_mod)

            if source:
                self.text = source

            else:
                self.text = tk.StringVar()
            self.value.config(textvariable=self.text)

            if text:
                self.value.config(text=text)

        self.separator = ttk.Separator(self.frame, orient=tk.HORIZONTAL)

        self.label = tk.Label(self.frame,
                              text=label_text,
                              font=default_font + " 10 italic")

        self.value.grid(row=0)
        self.separator.grid(row=1, sticky="EW")
        self.label.grid(row=2)

        if grid:
            self.grid(grid)
        elif pack:
            self.pack(pack)

    def pack(self, kwargs):
        self.frame.pack(kwargs)

    def grid(self, kwargs):
        self.frame.grid(kwargs, sticky="S", padx=4, pady=4)

    def update(self):
        pass

        # print(self.source.update())
        # print(self.text.get())
        # print(self.text)
        # print(char.info["name"].textvariable)
        # self.set(update_text)

class CharacterManager:
    """Converts a character data format into tkinter variables for use by
    the character sheet. Should eventually work both ways, allowing editing of values."""

    class DisplayValue:

        def __init__(self):
            self.add_display_value()

        def add_display_value(self):
            self.disp = tk.StringVar()
            self.disp.set(self.val)

        def get(self):
            pass

        def set(self):
            pass

    class SingleSourceValue(DisplayValue):
        def __init__(self, char):
            self.val = helpers.list_as_keys(char.data, self.source)
            super().__init__()

    ### Actual Aspects
    """Updatable defines if something is a base value or not, hence if it can 
    be updated or set without worrying about breaking something.
    Source points to the relevant location(s) in the character data dictionary"""

    class Name(SingleSourceValue):
        updatable = True
        source = ["info", "name"]
        def __init__(self, char):
            super().__init__(char)

    class Race(DisplayValue):
        updatable = False
        source = (["info", "race"],
                  ["info", "subrace"])
        def __init__(self, char):
            values = []
            for source in self.source:
                values.append(helpers.list_as_keys(char.data, source))
            values[-1] = f"({values[-1]})"
            self.val = " ".join(values)
            super().__init__()

    class Level(SingleSourceValue):
        updatable = False
        source = ["stats", "level"]
        def __init__(self, char):
            super().__init__(char)

    class Alignment(DisplayValue):
        updatable = True
        source = (["info", "ethics"],
                  ["info", "morality"])
        def __init__(self, char):
            values = []
            for source in self.source:
                values.append(helpers.list_as_keys(char.data, source))
            self.val = " ".join(values)
            super().__init__()

    class Size(SingleSourceValue):
        updatable = False
        source = ["stats", "size", "current"]
        def __init__(self, char):
            super().__init__(char)

    class Speed(SingleSourceValue):
        updatable = False
        source = ["stats", "speed", "current"]
        def __init__(self, char):
            super().__init__(char)

    class Faith(SingleSourceValue):
        updatable = True
        source = ["info", "faith"]
        def __init__(self, char):
            super().__init__(char)

    class Skin(SingleSourceValue):
        updatable = True
        source = ["info", "skin colour"]
        def __init__(self, char):
            super().__init__(char)

    class Hair(SingleSourceValue):
        updatable = True
        source = ["info", "hair colour"]
        def __init__(self, char):
            super().__init__(char)

    class Eyes(SingleSourceValue):
        updatable = True
        source = ["info", "eye colour"]
        def __init__(self, char):
            super().__init__(char)

    class Height(SingleSourceValue):
        updatable = True
        source = ["info", "height"]
        def __init__(self, char):
            super().__init__(char)

    class Weight(SingleSourceValue):
        updatable = True
        source = ["info", "weight"]
        def __init__(self, char):
            super().__init__(char)

    class Build(SingleSourceValue):
        updatable = True
        source = ["info", "build"]
        def __init__(self, char):
            super().__init__(char)

    class Age(SingleSourceValue):
        updatable = True
        source = ["info", "age"]
        def __init__(self, char):
            super().__init__(char)

    class Gender(SingleSourceValue):
        updatable = True
        source = ["info", "gender"]
        def __init__(self, char):
            super().__init__(char)

    aspects = {"name": Name,
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

    class Attr:
        source = ["ability scores"]
        def __init__(self, attr, char):
            pass

    # Should probably make this better at just being automatically updated

    def __init__(self, char):

        self.char = char

        for aspect, object in self.aspects.items():
            setattr(self, aspect, object(char))

        for attr in glossary.attrs:
            setattr(self, attr, self.Attr(attr, char))

        # for aspect in self.aspects.keys():
        #     # try:
        #     getattr(self, aspect).disp.get()
            # except AttributeError:
            #     print(F"{aspect.capitalize()} not fully implemented in converter.")

        # pass



class CharacterSheet:

    def __init__(self, window):
        self.master = window
        window.title("Character Sheet")

        character = Character()
        self.char = CharacterManager(character)
        # Utility Functions

        self.create_title()
        self.create_tab_manager()
        self.create_front_page()

        # Move window to centre

        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()
        position_right = int(window.winfo_screenwidth() / 5) - windowWidth
        position_down = int(window.winfo_screenheight() / 5) - windowHeight
        position_down = 0
        window.geometry(f"+{position_right}+{position_down}")

    def full_reset(self):
        self.master.destroy()
        window = tk.Tk()
        self.__init__(window)

        style = ttk.Style(window)
        style.configure('TNotebook', tabposition='n')

        # style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        # style.map('TCombobox', selectbackground=[('readonly', 'white')])
        # style.map('TCombobox', selectforeground=[('readonly', 'black')])
        # style.map('TCombobox', selectborderwidth=[('readonly', '0')])

        window.mainloop()

    def save(self):
        #     name = char.info["name"].get()
        #
        #     if name == "":
        #         name = "Empty_Character"
        #
        #     loc = f'saves/active_characters/{name}'
        #
        #     char.save(loc)
        pass

    def load(self):
        #
        #     current_directory = os.getcwd()
        #
        #     preferred_path = current_directory + "/saves/active_characters"
        #     backup_path = current_directory + "/saves/base_characters"
        #
        #     dir = os.listdir(preferred_path)
        #
        #     if len(dir) == 0:
        #         path = backup_path
        #         type = "base_character"
        #     else:
        #         path = preferred_path
        #         type = "active_character"
        #
        #     filename = tk.filedialog.askopenfilename(initialdir=path,
        #                                              title="Select save file",
        #                                              filetypes=(
        #                                                  ("Pickled Files", "*.pkl"),
        #                                                  ("all files", "*.*")))
        #
        #     # char.load(filename, type)
        #
        #     # current_directory = os.getcwd()
        #     #
        #     # filename = current_directory + "/saves/base_characters/Ser Gorden Simpleton.pkl"
        #
        #     self.exit()
        #
        #     startup(filename)
        #
        #     self.update()
        pass

    def refresh(self):
        pass

    def exit(self):
        self.master.destroy()

    def update(self):
        # for ID, object in self.updatables.items():
        #     try:
        #         object.update()
        #     except AttributeError:
        #         print(f"Error updating {ID} as it has no update method.")
        #
        # if hasattr(self, "tab_manager"):
        #     self.resize_tabs()
        pass

        # UI Methods

    def create_title(self):
        self.title = tk.Label(self.master,
                              text='Character Sheet',
                              bd=8,
                              font=default_font + " 14 bold")

        self.title.pack(side=tk.TOP)

        self.main_menu = tk.Menu(self.master)

        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_command(label="Refresh", command=self.refresh)
        # self.file_menu.add_command(label="Sanitise", command=self.sanitise)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.main_menu)

    def create_tab_manager(self):
        self.tab_manager = ttk.Notebook(self.master)

        self.stats_tab = ttk.Frame(self.tab_manager,
                                   relief=tk.FLAT,
                                   borderwidth=5)

        # self.class_tab = ttk.Frame(self.tab_manager,
        #                            relief=tk.FLAT,
        #                            borderwidth=5)

        self.tab_manager.add(self.stats_tab, text="Stats")
        # self.tab_manager.add(self.class_tab, text="Placeholder")

        self.tab_manager.bind("<<NotebookTabChanged>>", self.changed_tabs)

        self.tab_manager.pack()

    def changed_tabs(self, event):
        event.widget.update_idletasks()
        current_tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=current_tab.winfo_reqheight(),
                               width=current_tab.winfo_reqwidth())

        self.master.update_idletasks()
        self.tab_manager.update_idletasks()
        if self.master.winfo_width() > self.tab_manager.winfo_reqwidth():
            self.tab_manager.configure(width=self.master.winfo_width())

            current_tab_contents = \
                self.tab_manager.nametowidget(self.tab_manager.select()).winfo_children()[0]

            current_tab_contents.pack(fill="both", expand=True)

    def resize_tabs(self):
        self.tab_manager.update_idletasks()
        current_tab = self.tab_manager.nametowidget(self.tab_manager.select())
        self.tab_manager.configure(height=current_tab.winfo_reqheight(),
                                   width=current_tab.winfo_reqwidth())

    # Front Page Methods

    def create_front_page(self):
        self.front_page_frame = tk.Frame(self.stats_tab,
                                         relief=tk.SUNKEN,
                                         bd=4)

        front_page_column_1 = tk.Frame(self.front_page_frame)

        self.info_section(front_page_column_1).grid(row=0, column=0, columnspan=3, pady=4, padx=4, sticky="NW")

        # self.health_section(front_page_column_1).grid(row=1, column=0, columnspan=3, pady=4, padx=4, sticky="NEW")
        #
        # self.defences_section(front_page_column_1).grid(row=2, column=0, columnspan=3, pady=4, padx=4, sticky="NEW")
        #
        self.scores_section(front_page_column_1).grid(row=3, column=0, pady=4, padx=4, sticky="NSW")
        # self.saves_section(front_page_column_1).grid(row=3, column=1, pady=4, padx=4, sticky="NSW")
        # self.other_skills_section(front_page_column_1).grid(row=3, column=2, pady=4, padx=4, sticky="NW")
        #
        # self.skills_section(front_page_column_1).grid(row=4, column=0, columnspan=3, pady=4, padx=4, sticky="NSEW")
        #
        # front_page_column_2 = tk.Frame(self.front_page_frame)
        # self.class_section(front_page_column_2).grid(row=0, column=0, pady=4, padx=4, sticky="NEW")
        # self.proficiencies_section(front_page_column_2).grid(row=1, column=0, pady=4, padx=4, sticky="NEW")
        #
        # self.items_section(front_page_column_2).grid(row=2, column=0, pady=4, padx=4, sticky="NEWS")
        #
        # front_page_column_2.grid_rowconfigure(0, weight=1)

        front_page_column_1.grid(row=0, column=0, sticky="N")
        # front_page_column_2.grid(row=0, column=1, sticky="N")

        self.front_page_frame.pack(fill="both", expand=True)

        # for frame in [front_page_column_1, front_page_column_2]:
        for frame in [front_page_column_1]:

            for column in range(self.front_page_frame.grid_size()[0]):
                frame.grid_columnconfigure(column, weight=1)
            for row in range(self.front_page_frame.grid_size()[1]):
                frame.grid_rowconfigure(row, weight=1)

    def info_section(self, master_frame):
        self.info_frame = tk.Frame(master_frame,
                                   relief=tk.GROOVE,
                                   borderwidth=2)

        info_frame_rows = {0: tk.Frame(self.info_frame),
                           1: tk.Frame(self.info_frame),
                           2: tk.Frame(self.info_frame),
                           3: tk.Frame(self.info_frame),
                           }

        info_frame_dict = {"Name": (0, self.char.name, dict(font_mod=" 10 bold")),
                           "Race": (0, self.char.race),
                           "Level": (0, self.char.level),
                           "Alignment": (1, self.char.alignment),
                           "Size": (1, self.char.size),
                           "Speed": (1, self.char.speed),
                           "Faith": (1, self.char.faith),
                           "Skin": (2, self.char.skin),
                           "Hair": (2, self.char.hair),
                           "Eyes": (2, self.char.eyes),
                           "Height": (2, self.char.height),
                           "Weight": (2, self.char.weight),
                           "Build": (2, self.char.build),
                           "Age": (2, self.char.age),
                           "Gender": (2, self.char.gender),
                           }

        row_length = {0: 0,
                      1: 0,
                      2: 0,
                      3: 0}

        for name, vals in info_frame_dict.items():
            font_mod = None
            row = vals[0] + 1
            source = vals[1]

            if len(vals) > 2:
                font_mod = vals[2]["font_mod"]

            row_frame = info_frame_rows[row]

            Info_Value_Pair(master_frame=row_frame,
                            label_text=name,
                            text_font_mod=font_mod,
                            source=source.disp,
                            grid=dict(row=0, column=row_length[row], padx=4))

            row_length[row] += 1

        max_columns = 0

        for row, frame in info_frame_rows.items():
            frame.grid(row=row, sticky="EW")
            if frame.grid_size()[0] > max_columns:
                max_columns = frame.grid_size()[0]
            # for n in range(frame.grid_size()[0]):
            for n in range(4):
                frame.grid_columnconfigure(n, weight=1)

        tk.Label(info_frame_rows[0],
                 text="Character Info",
                 font=default_font + " 12 bold",
                 anchor=tk.CENTER).grid(row=0, column=0, columnspan=max_columns, sticky="EW")

        return self.info_frame

    def scores_section(self, master_frame):

        self.scores_frame = tk.Frame(master_frame,
                                     relief=tk.GROOVE,
                                     borderwidth=2)

        tk.Label(self.scores_frame,
                 text="Ability Scores",
                 font=default_font + " 11 bold").grid(row=0, columnspan=3, padx=4)

        self.ability_scores_raw = {}

        for n, attr in enumerate(glossary.attrs):
            n = n + 1
            tk.Label(self.scores_frame,
                     text=attr,
                     font=default_font + " 10 bold").grid(row=n, column=0, padx=2)

            object_name = f"ability_score_raw_{attr.lower()}"

            # button_frame = tk.Frame(self.scores_frame,
            #                         relief=tk.GROOVE,
            #                         borderwidth=2)
            # button_frame.grid(row=2, column=n, padx=2)

            # n = 0
            tk.Button(self.scores_frame,
                      textvariable=char.ability_scores[attr].raw,
                      relief=tk.FLAT,
                      borderwidth=1,
                      font=default_font + " 10",
                      height=1,
                      width=3).grid(row=n, column=1)

            # ttk.Separator(button_frame, orient=tk.HORIZONTAL).grid(row=3, column=n, columnspan=1, sticky="ew")

            tk.Button(self.scores_frame,
                      textvariable=char.ability_scores[attr].mod,
                      font=default_font + " 10 bold",
                      relief=tk.FLAT,
                      borderwidth=1,
                      height=1,
                      width=3).grid(row=n, column=2)

        ttk.Separator(self.scores_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=6, sticky="NEW")

        return self.scores_frame


def startup(load=None):
    window = tk.Tk()

    CharacterSheet(window)

    style = ttk.Style(window)
    style.configure('TNotebook', tabposition='n')

    if platform == "linux":
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])
        style.map('TCombobox', selectborderwidth=[('readonly', '0')])

    window.mainloop()


if __name__ == "__main__":
    startup()
