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

import Character_Sheet.character_manager as cm
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


class CharacterSheet:

    def __init__(self, window):
        self.master = window
        window.title("Character Sheet")

        self.char = cm.char
        self.aspects = cm.Aspects()

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

        self.health_section(front_page_column_1).grid(row=1, column=0, columnspan=3, pady=4, padx=4, sticky="NEW")

        # self.defences_section(front_page_column_1).grid(row=2, column=0, columnspan=3, pady=4, padx=4, sticky="NEW")

        self.scores_section(front_page_column_1).grid(row=3, column=0, pady=4, padx=4, sticky="NSW")
        self.saves_section(front_page_column_1).grid(row=3, column=1, pady=4, padx=4, sticky="NSW")
        self.other_skills_section(front_page_column_1).grid(row=3, column=2, pady=4, padx=4, sticky="NW")

        self.skills_section(front_page_column_1).grid(row=4, column=0, columnspan=3, pady=4, padx=4, sticky="NSEW")

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

        info_frame_dict = {"Name": (0, self.aspects.name, dict(font_mod=" 10 bold")),
                           "Race": (0, self.aspects.race),
                           "Level": (0, self.aspects.level),
                           "Alignment": (1, self.aspects.alignment),
                           "Size": (1, self.aspects.size),
                           "Speed": (1, self.aspects.speed),
                           "Faith": (1, self.aspects.faith),
                           "Skin": (2, self.aspects.skin),
                           "Hair": (2, self.aspects.hair),
                           "Eyes": (2, self.aspects.eyes),
                           "Height": (2, self.aspects.height),
                           "Weight": (2, self.aspects.weight),
                           "Build": (2, self.aspects.build),
                           "Age": (2, self.aspects.age),
                           "Gender": (2, self.aspects.gender),
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
                            source=source.tkVar,
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
                      textvariable=getattr(self.aspects, attr)["raw"].tkVar,
                      relief=tk.FLAT,
                      borderwidth=1,
                      font=default_font + " 10",
                      height=1,
                      width=3).grid(row=n, column=1)

            # ttk.Separator(button_frame, orient=tk.HORIZONTAL).grid(row=3, column=n, columnspan=1, sticky="ew")

            tk.Button(self.scores_frame,
                      textvariable=getattr(self.aspects, attr)["mod"].tkVar,
                      font=default_font + " 10 bold",
                      relief=tk.FLAT,
                      borderwidth=1,
                      height=1,
                      width=3).grid(row=n, column=2)

        ttk.Separator(self.scores_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=6, sticky="NEW")

        return self.scores_frame

    def saves_section(self, master_frame):

        self.saves_frame = tk.Frame(master_frame,
                                    relief=tk.GROOVE,
                                    borderwidth=2)

        tk.Label(self.saves_frame,
                 text="Saving Throws",
                 font=default_font + " 11 bold").grid(row=0, columnspan=2)

        self.ability_scores_raw = {}

        for n, attr in enumerate(glossary.attrs):
            n = n + 1
            # tk.Label(self.saves_frame,
            #          text=attr,
            #          font=default_font + " 10 bold").grid(row=n, column=0, padx=4, pady=0)

            object_name = f"ability_score_raw_{attr.lower()}"

            def toggle(cb):
                cb.toggle()

            cb = tk.Checkbutton(self.saves_frame,
                                variable=getattr(self.aspects, attr)["save prof"].tkVar,
                                text=attr,
                                font=default_font + " 10 bold")

            cb.config(command=partial(toggle, cb))

            cb.grid(row=n, column=0, sticky="W")

            tk.Button(self.saves_frame,
                      textvariable=getattr(self.aspects, attr)["save val"].tkVar,  # Must make save separate
                      relief=tk.FLAT,
                      borderwidth=2,
                      font=default_font + " 9 bold",
                      width=3).grid(row=n, column=1)

        ttk.Separator(self.saves_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=10, sticky="NEW")

        return self.saves_frame

    def skills_section(self, master_frame):

        self.skills_frame = tk.Frame(master_frame,
                                     relief=tk.GROOVE,
                                     borderwidth=2)

        num_skills = len(skills.skills_list)

        for n, skill in enumerate(skills.skills_list.values()):

            def toggle(cb):
                cb.toggle()

            cb = tk.Checkbutton(self.skills_frame,
                                variable=getattr(self.aspects, skill.name.lower())["prof"].tkVar,
                                textvariable=getattr(self.aspects, skill.name.lower())["val"].tkVar,
                                font=default_font + " 10 bold",
                                anchor=tk.W
                                )

            lb = tk.Label(self.skills_frame,
                          text=F"{skill.name} ({skill.attr.__name__})",
                          font=default_font + " 10",
                          anchor=tk.E)

            cb.config(command=partial(toggle, cb))

            if n < num_skills / 2:
                cb.grid(row=n + 1, column=1, sticky="EW")
                lb.grid(row=n + 1, column=0, sticky="EW")
            else:
                cb.grid(row=int(n + 1 - num_skills / 2), column=4, sticky="EW")
                lb.grid(row=int(n + 1 - num_skills / 2), column=3, sticky="EW")

        frame_width, frame_height = self.skills_frame.grid_size()

        tk.Label(self.skills_frame,
                 text="Skills",
                 font=default_font + " 11 bold").grid(row=0, column=0, columnspan=frame_width)

        ttk.Separator(self.skills_frame, orient=tk.VERTICAL).grid(row=1, column=2, rowspan=frame_height, sticky="NS",
                                                                  padx=4)
        ttk.Separator(self.skills_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=frame_width,
                                                                    sticky="NEW")

        for n in range(frame_width):
            self.skills_frame.columnconfigure(n, weight=1)
        for n in range(frame_height):
            self.skills_frame.rowconfigure(n, weight=1)

        return self.skills_frame

    def other_skills_section(self, master_frame):

        self.other_skills_frame = tk.Frame(master_frame,
                                           relief=tk.GROOVE,
                                           borderwidth=2)

        tk.Label(self.other_skills_frame,
                 text="Checks:",
                 justify=tk.LEFT,
                 font=default_font + " 11 bold").grid(row=0, column=0, columnspan=2, sticky="NEW")

        ttk.Separator(self.other_skills_frame,
                      orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="EW")

        tk.Label(self.other_skills_frame,
                 text="Proficiency Bonus:",
                 justify=tk.LEFT,
                 font=default_font + " 10 ").grid(row=2, column=0, sticky="W")

        tk.Label(self.other_skills_frame,
                 textvariable=self.aspects.proficiency_bonus.tkVar,
                 font=default_font + " 10 bold").grid(row=2, column=1, sticky="E")

        tk.Label(self.other_skills_frame,
                 text="Initiative:",
                 justify=tk.LEFT,
                 font=default_font + " 10 ").grid(row=3, column=0, sticky="W")

        tk.Label(self.other_skills_frame,
                 textvariable=self.aspects.DEX["mod"].tkVar,
                 font=default_font + " 10 bold").grid(row=3, column=1, sticky="E")

        ttk.Separator(self.other_skills_frame,
                      orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky="EW")

        tk.Label(self.other_skills_frame,
                 text="Senses:",
                 justify=tk.LEFT,
                 font=default_font + " 11 bold").grid(row=5, column=0, columnspan=2, sticky="NEW")

        ttk.Separator(self.other_skills_frame,
                      orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky="EW")

        tk.Label(self.other_skills_frame,
                 text="Passive Perception:",
                 justify=tk.LEFT,
                 font=default_font + " 10 ").grid(row=7, column=0, sticky="W")

        tk.Label(self.other_skills_frame,
                 textvariable=self.aspects.passive_perception.tkVar,
                 font=default_font + " 10 bold").grid(row=7, column=1, sticky="E")

        tk.Label(self.other_skills_frame,
                 text="Passive Investigation:",
                 justify=tk.LEFT,
                 font=default_font + " 10 ").grid(row=8, column=0, sticky="W")

        tk.Label(self.other_skills_frame,
                 textvariable=self.aspects.passive_investigation.tkVar,
                 font=default_font + " 10 bold").grid(row=8, column=1, sticky="E")

        tk.Label(self.other_skills_frame,
                 text="Passive Insight:",
                 justify=tk.LEFT,
                 font=default_font + " 10 ").grid(row=9, column=0, sticky="W")

        tk.Label(self.other_skills_frame,
                 textvariable=self.aspects.passive_insight.tkVar,
                 font=default_font + " 10 bold").grid(row=9, column=1, sticky="E")

        return self.other_skills_frame

    def health_section(self, master_frame):

        self.health_frame = tk.Frame(master_frame,
                                     relief=tk.GROOVE,
                                     bd=2)

        # self.deaths_frame = tk.Frame(self.health_frame,
        #                              relief=tk.GROOVE,
        #                              bd=2)
        # self.deaths_frame.grid(row=0, column=0)

        tk.Label(self.health_frame,
                 text="Death Saving Throws",
                 font=default_font + " 10 bold").grid(row=0, column=0, columnspan=5, sticky="EW")

        cv = tk.Canvas(self.health_frame,
                       relief=tk.GROOVE,
                       bd=2,
                       height=44, width=44)

        cv.grid(row=1, column=0, rowspan=2, sticky="W")

        cvtext = cv.create_text(28, 28, text=":)",
                                angle=-90,
                                font=default_font + " 24 bold",
                                anchor=tk.CENTER)

        # cv.itemconfigure(cvtext, text=":(")
        cv.itemconfigure(cvtext, state=tk.HIDDEN)

        tk.Label(self.health_frame,
                 text="Sucess",
                 font=default_font + " 9",
                 ).grid(row=1, column=1, sticky="S")
        tk.Label(self.health_frame,
                 text="Fail",
                 font=default_font + " 9",
                 ).grid(row=2, column=1, sticky="N")

        class DeathSavesManager:
            def __init__(self, HP, widgets, cv_pack, name):
                self.widgets = widgets
                cv, cvtext = cv_pack
                self.cv = cv
                self.cvtext = cvtext
                self.current_hp, self.max_hp, self.temp_hp = HP
                self.active = False
                self.name = name

            def activate(self, instant_death=False):

                for widget in self.widgets:
                    widget.config(state=tk.NORMAL)
                    widget.deselect()
                if instant_death:
                    cv.itemconfigure(cvtext, text="X(")
                    self.death(instant=True)
                    self.deactivate()
                else:
                    cv.itemconfigure(cvtext, text=":|")
                    self.active = True

                cv.itemconfigure(cvtext, state=tk.NORMAL)

            def deactivate(self):

                for widget in self.widgets:
                    widget.config(state=tk.DISABLED)
                    widget.deselect()
                cv.itemconfigure(cvtext, state=tk.HIDDEN)

                self.active = False

            def heal(self, val):

                current_hp = self.current_hp.update().tkVar.get()
                max_hp = self.max_hp.update().tkVar.get()
                change = val.get()
                new_current = current_hp + change
                if new_current > max_hp:
                    new_current = max_hp
                if new_current > 0:
                    self.deactivate()
                self.current_hp.change_value(new_current)
                val.set(0)

            def harm(self, val):

                current_hp = self.current_hp.update().tkVar.get()
                temp_hp = self.temp_hp.update().tkVar.get()
                change = val.get()
                if temp_hp > 0:
                    new_temp = temp_hp - change
                    if new_temp > 0:
                        self.temp_hp.change_value(new_temp)
                        change = 0
                    else:
                        self.temp_hp.change_value(0)
                        change = abs(new_temp)
                new_current = current_hp - change
                self.current_hp.change_value(new_current)
                val.set(0)

                # Saving throw / Deaths
                if new_current <= 0:
                    new_current = 0
                    self.current_hp.change_value(new_current)
                    if change >= current_hp + self.max_hp.update().tkVar.get():
                        self.activate(instant_death=True)
                    else:
                        self.activate(instant_death=False)

            def death_save_change(self, death_save_vals):

                passes = death_save_vals["passed"]
                fails = death_save_vals["failed"]

                num_passes = sum([val.tkVar.get() for val in passes.values()])
                num_fails = sum([val.tkVar.get() for val in fails.values()])

                lookup_dict = {2: ":D",
                               1: ":)",
                               0: ":|",
                               -1: ":/",
                               -2: ":("}

                if num_fails == 3:
                    cv.itemconfigure(cvtext, text="X(")
                    self.death(instant=False)
                elif num_passes == 3:
                    if platform == "windows":
                        cv.itemconfigure(cvtext, text="🎉")
                    elif platform == "linux":
                        cv.itemconfigure(cvtext, text="")
                    heal_val = tk.IntVar()
                    heal_val.set(1)
                    self.heal(heal_val)
                elif num_passes == 2 and num_fails == 2:
                    cv.itemconfigure(cvtext, text=":O")
                elif num_passes == 2:
                    cv.itemconfigure(cvtext, text=":D")
                elif num_fails == 2:
                    cv.itemconfigure(cvtext, text=":(")
                else:
                    cv.itemconfigure(cvtext, text=lookup_dict[num_passes - num_fails])

            def death(self, instant=False):
                print("You have died!")

                death_window = tk.Tk()
                windowWidth = death_window.winfo_reqwidth()
                windowHeight = death_window.winfo_reqheight()
                position_right = int(death_window.winfo_screenwidth() / 3 - windowWidth / 2)
                position_down = int(death_window.winfo_screenheight() / 2 - windowHeight / 2)
                death_window.geometry(f"+{position_right}+{position_down}")
                if instant:
                    text = "Oh no! You have died due to taking an exessive amount of damage!"
                else:
                    text = "Oh no! You have failed 3 death saving throws and have died!"

                text += f"\n\nIf your party cannot find a way to revive you, unfortunately this is the end for {self.name.tkVar.get()}.\nWhile this is naturally very sad, it does mean you have a chance to create a whole new character, with new hopes and dreams and skills. Maybe try to take better care of this one.\n\n Happy adventuring!"

                tk.Label(death_window,
                         text=text,
                         wraplength=420).pack(pady=8, padx=8)

            def check(self, *_):
                current_hp = self.current_hp.update().tkVar.get()

                if current_hp <= 0 and self.active == False:
                    self.activate()
                elif current_hp > 0 and self.active == True:
                    self.deactivate()

        self.death_save_widgets = []

        hp_set = (
            self.aspects.current_HP,
            self.aspects.max_HP,
            self.aspects.temp_HP
        )

        death_saves_mgmt = DeathSavesManager(hp_set, self.death_save_widgets, (cv, cvtext), self.aspects.name)

        for row in [1, 2]:
            for n, column in enumerate([2, 3, 4]):
                if row == 1:
                    s = "S"
                    origin = self.aspects.death_saves["passed"]
                if row == 2:
                    s = "N"
                    origin = self.aspects.death_saves["failed"]

                cb = tk.Checkbutton(self.health_frame,
                                    command=partial(death_saves_mgmt.death_save_change, self.aspects.death_saves),
                                    variable=origin[n].tkVar,
                                    state=tk.DISABLED)

                cb.grid(row=row, column=column, sticky=s)

                self.death_save_widgets.append(cb)

        frame_width, frame_height = self.health_frame.grid_size()

        ttk.Separator(self.health_frame, orient=tk.VERTICAL).grid(row=0,
                                                                  column=frame_width,
                                                                  rowspan=4,
                                                                  sticky="NSW",
                                                                  padx=2)

        frame_width, frame_height = self.health_frame.grid_size()

        tk.Label(self.health_frame,
                 text="Hit Points",
                 font=default_font + " 10 bold").grid(row=0, column=frame_width, columnspan=2)

        hp_frame = tk.Frame(self.health_frame)
        hp_frame.grid(row=1, column=frame_width, rowspan=2, padx=4, pady=4)

        tk.Label(hp_frame,
                 textvariable=self.aspects.current_HP.tkVar,
                 font=default_font + " 12 bold").grid(row=0, column=0)

        ttk.Separator(hp_frame,
                      orient=tk.HORIZONTAL).grid(row=1, column=0, sticky="EW")

        tk.Label(hp_frame,
                 textvariable=self.aspects.max_HP.tkVar,
                 font=default_font + " 12 bold").grid(row=2, column=0)

        hp_change_frame = tk.Frame(self.health_frame)
        hp_change_frame.grid(row=1, column=frame_width + 1, rowspan=2, padx=4, pady=4)

        hp_change_var = tk.IntVar()

        hp_change = tk.Entry(hp_change_frame,
                             textvariable=hp_change_var,
                             width=4,
                             justify=tk.CENTER,
                             font=default_font + " 10",
                             )
        hp_change.grid(row=1, column=0, padx=4)

        tk.Button(hp_change_frame,
                  text="Heal",
                  command=partial(death_saves_mgmt.heal, hp_change_var)
                  ).grid(row=0, column=0, padx=4)

        tk.Button(hp_change_frame,
                  text="Harm",
                  command=partial(death_saves_mgmt.harm, hp_change_var)
                  ).grid(row=2, column=0, padx=4)

        # Probably add this to the character tracker instead. Make that manage the death saves, this just displays them remember.

        # row, column = self.health_frame.grid_size()
        # for r in range(row):
        #     self.health_frame.rowconfigure(r, weight=1)
        # for c in range(column):
        #     self.health_frame.columnconfigure(c, weight=1)

        ttk.Separator(self.health_frame,
                      orient=tk.VERTICAL).grid(row=0, column=frame_width + 2, rowspan=4, padx=4, sticky="NS")

        rest_frame = tk.Frame(self.health_frame)
        rest_frame.grid(row=0, column=frame_width + 3, rowspan=3, padx=4, pady=4)

        self.aspects.current_HP.tkVar.trace_add("write", death_saves_mgmt.check)

        lr_text = "Long Rest"
        sr_text = "Short Rest"
        if platform == "windows":
            lr_text += " 🛏"
            sr_text += " 🔥"

        tk.Button(rest_frame,
                  text=lr_text,
                  # command=char.long_rest,
                  font=default_font + " 9 ").grid(row=1, column=0, columnspan=2, sticky="EW", pady=4)

        tk.Button(rest_frame,
                  text=sr_text,
                  # command=char.short_rest,
                  font=default_font + " 9 ").grid(row=0, column=0, columnspan=2, sticky="EW", pady=4)

        tk.Label(rest_frame,
                 text="Temp HP:",
                 font=default_font + " 9").grid(row=2, column=0, pady=4)
        tk.Entry(rest_frame,
                 font=default_font + " 9",
                 textvariable=self.aspects.temp_HP.tkVar,
                 width=3,
                 justify=tk.CENTER).grid(row=2, column=1)

        helpers.weight_frame(self.health_frame)

        for column in range(5):
            self.health_frame.columnconfigure(column, weight=0)

        return self.health_frame

    def defences_section(self, master_frame):
        defences_frame = tk.Frame(master_frame, )

        ac_frame = tk.Frame(defences_frame,
                            relief=tk.GROOVE,
                            bd=2)
        ac_frame.grid(row=0, column=0, padx=8)
        tk.Label(ac_frame,
                 text="Armour Class",
                 font=default_font + " 10 bold",
                 justify=tk.CENTER).grid(row=0, column=0, sticky="N", padx=4)

        shieldpath = Path.cwd() / "reference" / "images" / "shield.png"

        shield_im = Image.open(shieldpath)
        shield_im.thumbnail((44, 44), Image.ANTIALIAS)

        self.shield_im = ImageTk.PhotoImage(shield_im.convert('RGBA'))

        tk.Button(ac_frame,
                  textvariable=char.AC.val,
                  relief=tk.FLAT,
                  # width=2,
                  # height=1,
                  image=self.shield_im,
                  compound="center",
                  font=default_font + " 12 bold").grid(row=1, column=0, sticky="NEWS", padx=4, pady=4)

        def get_armours():
            wearable = ["None"]
            for item in char.inventory["items"]:
                if isinstance(item, (Light, Medium, Heavy)):
                    wearable.append(item.name)

            armour_choice["values"] = wearable

        armour_choice = ttk.Combobox(ac_frame,
                                     state="readonly",
                                     postcommand=get_armours,
                                     width=16,
                                     textvariable=char.inventory["worn"],
                                     font=default_font + " 10",
                                     justify=tk.CENTER)
        armour_choice.grid(row=2, column=0, padx=4, pady=(0, 4))

        def armour_chosen(*_):
            char.update_all()

        char.inventory["worn"].trace_add("write", armour_chosen)

        ### Defences and Conditions Frame

        defences_and_conditions_frame = tk.Frame(defences_frame,
                                                 relief=tk.GROOVE,
                                                 bd=2)
        defences_and_conditions_frame.grid(row=0, column=1, columnspan=2, padx=8, sticky="NEW")

        tk.Label(defences_and_conditions_frame,
                 text="Defences",
                 font=default_font + " 11 bold",
                 justify=tk.CENTER,
                 anchor=tk.CENTER).grid(row=0, column=0, sticky="NEW", padx=4)

        tk.Label(defences_and_conditions_frame,
                 text="Conditions",
                 font=default_font + " 11 bold",
                 justify=tk.CENTER,
                 anchor=tk.CENTER).grid(row=0, column=2, sticky="NEW", padx=4)

        ttk.Separator(defences_and_conditions_frame,
                      orient=tk.VERTICAL).grid(row=0, column=1, rowspan=4, sticky="NS")

        ttk.Separator(defences_and_conditions_frame,
                      orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky="NEW")

        defences = tk.Frame(defences_and_conditions_frame)
        tk.Label(defences,
                 textvariable=char.defence_string.string,
                 font=default_font + " 9",
                 anchor=tk.CENTER,
                 justify=tk.CENTER).pack()
        defences.grid(row=2, column=0, sticky="N")

        conditions = tk.Frame(defences_and_conditions_frame)
        tk.Label(conditions,
                 textvariable=char.conditions_string.string,
                 font=default_font + " 9",
                 anchor=tk.CENTER,
                 justify=tk.CENTER).pack()
        conditions.grid(row=2, column=2, sticky="N")

        helpers.weight_frame(defences)
        helpers.weight_frame(conditions)
        helpers.weight_frame(defences_and_conditions_frame)
        defences_and_conditions_frame.columnconfigure(1, weight=0)
        helpers.weight_frame(defences_frame)

        return defences_frame

    def class_section(self, master_frame):

        self.class_frame = tk.Frame(master_frame,
                                    relief=tk.GROOVE,
                                    bd=2)

        tk.Label(self.class_frame,
                 text="Class",
                 font=default_font + " 12 bold",
                 justify=tk.CENTER).grid(row=0, column=0, sticky="EW")

        # tk.Label(self.class_frame,
        #          text="Level",
        #          font=default_font+" 10 bold",
        #          justify=tk.CENTER).grid(row=0, column=1)
        # tk.Label(self.class_frame,
        #          text="Subclass",
        #          font=default_font+" 10 bold",
        #          justify=tk.CENTER).grid(row=0, column=2)
        # tk.Label(self.class_frame,
        #          text="Hit Die",
        #          font=default_font+" 10 bold",
        #          justify=tk.CENTER).grid(row=0, column=3)

        helpers.weight_frame(self.class_frame)

        return self.class_frame

    def proficiencies_section(self, master_frame):
        self.proficiencies_frame = tk.Frame(master_frame,
                                            relief=tk.GROOVE,
                                            borderwidth=2)

        prof_frames_dict = {}

        for n, object in enumerate(["Armour", "S", "Weapons", "S", "Tools", "S", "Languages"]):
            if object != "S":
                tk.Label(self.proficiencies_frame,
                         text=object,
                         # width=8,
                         font=default_font + " 10 bold").grid(row=2, column=n, sticky="EW", padx=6)
                frame = tk.Frame(self.proficiencies_frame)
                frame.grid(row=4, column=n, sticky="N")
                prof_frames_dict[object] = frame

            else:
                ttk.Separator(self.proficiencies_frame,
                              orient=tk.VERTICAL).grid(row=2, rowspan=3, column=n, sticky="NS")

        frame_width = self.proficiencies_frame.grid_size()[0]

        tk.Label(self.proficiencies_frame,
                 text="Skills and Proficiencies",
                 font=default_font + " 11 bold").grid(row=0, column=0, columnspan=frame_width, sticky="N")

        ttk.Separator(self.proficiencies_frame,
                      orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=frame_width, sticky="EW")

        ttk.Separator(self.proficiencies_frame,
                      orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=frame_width, sticky="EW")

        armour_types = ["Light", "Medium", "Heavy"]
        weapon_types = ["Simple", "Martial", "Shields"]

        for prof_type, vals in [("Armour", armour_types), ("Weapons", weapon_types)]:
            for n, value in enumerate(vals):
                tk.Label(prof_frames_dict[prof_type],
                         text=value,
                         font=default_font + " 10").grid(row=n, column=0, sticky="W")

                def toggle(cb):
                    cb.toggle()

                cb = tk.Checkbutton(prof_frames_dict[prof_type],
                                    compound=tk.LEFT,
                                    variable=tk.BooleanVar())

                cb.config(command=partial(toggle, cb))

                cb.grid(row=n, column=1)

                if value in [prof.name for prof in char.proficiencies["Major"]]:
                    cb.toggle()

        for prof_type in ["Tools", "Languages"]:
            j = 0
            for name, prof in char.proficiencies[prof_type].items():
                if prof.update():
                    tk.Label(prof_frames_dict[prof_type],
                             text=name,
                             font=default_font + " 9").grid(row=j, column=0)
                    j += 1

        helpers.weight_frame(self.proficiencies_frame)

        return self.proficiencies_frame

    def items_section(self, master_frame):
        items_frame = tk.Frame(master_frame,
                               relief=tk.GROOVE,
                               bd=2,
                               padx=-2)

        tk.Label(items_frame,
                 text="Items",
                 font=default_font + " 11 bold",
                 justify=tk.CENTER,
                 anchor=tk.CENTER).grid(row=0, column=0, columnspan=5)

        ttk.Separator(items_frame,
                      orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=5, sticky="EW")

        ttk.Separator(items_frame, orient=tk.VERTICAL).grid(row=2, column=1, rowspan=5, sticky="NS")
        ttk.Separator(items_frame, orient=tk.VERTICAL).grid(row=2, column=3, rowspan=5, sticky="NS")
        ttk.Separator(items_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=5, sticky="EW")

        helpers.weight_frame(items_frame)
        items_frame.columnconfigure((1, 3), weight=0)

        def wielded():
            tk.Label(items_frame,
                     text="Wieldable",
                     font=default_font + " 10 italic",
                     justify=tk.CENTER,
                     anchor=tk.CENTER).grid(row=2, column=0)

            def get_wieldable(widget_num):

                widget_num -= 1

                wieldable = []
                two_handed = []
                for item in char.inventory["items"]:

                    # print(item.name, item.num)

                    if item.wieldable == True:
                        if hasattr(item, "properties"):
                            if "versatile" in item.properties.keys():
                                wieldable.append(item.name)
                                two_handed.append(F"{item.name}")
                            elif "two-handed" in item.properties.keys():
                                two_handed.append(F"{item.name}")
                            else:
                                wieldable.append(item.name)
                        else:
                            wieldable.append(item.name)

                widgets = [self.equipped_1, self.equipped_2]

                other_widget = widgets[1 - widget_num]
                chosen = other_widget.get()

                if " (2H)" in chosen:
                    chosen = chosen[:-5]

                if chosen:
                    try:
                        wieldable.remove(chosen)
                    except ValueError:
                        pass
                    try:
                        two_handed.remove(chosen)
                    except ValueError:
                        pass

                two_handed = [item + " (2H)" for item in two_handed]

                widgets[widget_num]["values"] = sorted(wieldable + two_handed)

            self.equipped_1 = ttk.Combobox(items_frame,
                                           justify=tk.CENTER,
                                           font=default_font + " 10",
                                           state="readonly",
                                           textvariable=char.inventory["wielded"][1],
                                           width=16)

            self.equipped_1.config(postcommand=partial(get_wieldable, 1), )

            self.equipped_1.grid(row=4, column=0, pady=1, padx=2)

            self.equipped_2 = ttk.Combobox(items_frame,
                                           justify=tk.CENTER,
                                           font=default_font + " 10",
                                           state="readonly",
                                           textvariable=char.inventory["wielded"][2],
                                           width=16)

            self.equipped_2.config(postcommand=partial(get_wieldable, 2), )

            self.equipped_2.grid(row=5, column=0, pady=1, padx=2)

            def wielded_change(index, char, *_):
                index -= 1

                widgets = [self.equipped_1, self.equipped_2]
                values = [char.Inventory["wielded"][1], char.Inventory["wielded"][2]]
                grid_vals = [dict(row=4, column=0, pady=1), dict(row=5, column=0, pady=1)]

                if " (2H)" in values[index].get():
                    widgets[1 - index].grid_forget()
                    values[1 - index].set("")
                else:
                    widgets[1 - index].grid(grid_vals[1 - index])
                char.update_all()

            char.inventory["wielded"][1].trace_add("write", partial(wielded_change, 1, char))
            char.inventory["wielded"][2].trace_add("write", partial(wielded_change, 2, char))

        def attuned():
            tk.Label(items_frame,
                     text="Attunable",
                     font=default_font + " 10 italic",
                     justify=tk.CENTER,
                     anchor=tk.CENTER).grid(row=2, column=2)

            self.attuned_1 = ttk.Combobox(items_frame,
                                          justify=tk.CENTER,
                                          font=default_font + " 10",
                                          state="readonly",
                                          width=16)

            self.attuned_1.grid(row=4, column=2, pady=1, padx=2)

            self.attuned_2 = ttk.Combobox(items_frame,
                                          justify=tk.CENTER,
                                          font=default_font + " 10",
                                          state="readonly",
                                          width=16)

            self.attuned_2.grid(row=5, column=2, pady=1, padx=2)

            self.attuned_3 = ttk.Combobox(items_frame,
                                          justify=tk.CENTER,
                                          font=default_font + " 10",
                                          state="readonly",
                                          width=16)

            self.attuned_3.grid(row=6, column=2, pady=1, padx=2)

        def currency():
            tk.Label(items_frame,
                     text="Currency",
                     font=default_font + " 10 italic",
                     justify=tk.CENTER,
                     anchor=tk.CENTER).grid(row=2, column=4)

            frame = tk.Frame(items_frame)
            frame.grid(row=4, column=4, rowspan=3, sticky="EW")

            for n, currency in enumerate([("Gold", "gp"), ("Silver", "sp"), ("Copper", "cp")]):
                name, ref = currency
                tk.Button(frame, text=F"{name}:",
                          font=default_font + " 10",
                          justify=tk.RIGHT,
                          relief=tk.FLAT,
                          anchor=tk.E).grid(row=n, column=0, sticky="WE")

                ref = char.inventory["currency"][ref]

                tk.Label(frame, textvariable=ref,
                         font=default_font + " 10",
                         justify=tk.RIGHT).grid(row=n, column=1, sticky="W")
                #
                # frame.columnconfigure(0, weight=2)
                # frame.columnconfigure(1, weight=1)

            ttk.Separator(items_frame,
                          orient=tk.HORIZONTAL).grid(row=7, column=0, columnspan=5, sticky="NEW")

        def notable():
            frame = tk.Frame(items_frame)

            frame_width, frame_height = items_frame.grid_size()

            frame.grid(row=frame_height, column=0, columnspan=frame_width, sticky="EW")

            tk.Label(frame,
                     text="Notable",
                     font=default_font + " 10 italic",
                     justify=tk.CENTER).grid(row=0, column=0)

            ttk.Separator(frame,
                          orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky="EW")

            tk.Label(frame,
                     text="Temporary (Quest)",
                     font=default_font + " 10 italic",
                     justify=tk.CENTER).grid(row=0, column=2)

            placeholder = tk.Label(frame,
                                   text="\n\n\n",
                                   justify=tk.LEFT).grid(row=2, column=0)

            ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=3, sticky="EW")

            tk.Label(frame,
                     text="Equippable",
                     font=default_font + " 10 italic").grid(row=4, column=0)

            tk.Label(frame,
                     text="Generic",
                     font=default_font + " 10 italic").grid(row=4, column=2)

            placeholder = tk.Label(frame,
                                   text="\n\n\n",
                                   justify=tk.LEFT).grid(row=6, column=0)

            ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=3, sticky="EW")

            frame_width, frame_height = items_frame.grid_size()

            ttk.Separator(frame,
                          orient=tk.VERTICAL).grid(row=0, column=1, rowspan=frame_height, sticky="NS")

            helpers.weight_frame(frame)

            frame.columnconfigure(0, weight=8)  # ? Why not 2
            frame.columnconfigure(1, weight=0)
            frame.columnconfigure(2, weight=1)

        wielded()
        attuned()
        currency()
        notable()

        return items_frame


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
    pass
