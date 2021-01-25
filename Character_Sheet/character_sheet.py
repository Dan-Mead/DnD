import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from functools import partial
import textwrap
import num2words

from Character_Sheet.character import Character
import Character_Sheet.reference.races as races
import Character_Sheet.reference.glossary as glossary

default_font = "Verdana"


def import_info(filename):
    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()
    return info


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
                 text_font_mod=None,
                 grid=None,
                 pack=None):

        self.frame = tk.Frame(master_frame)

        if value_type == ValueTypes.text:
            self.value = tk.Label(self.frame,
                                  font=default_font + " 10")
            if text_font_mod:
                self.value.config(font=default_font + text_font_mod)

            if text:
                self.value.config(text=text)

        self.separator = ttk.Separator(self.frame,
                                       orient=tk.HORIZONTAL)
        self.label = tk.Label(self.frame,
                              text=label_text,
                              font=default_font + " 10 italic")

        self.value.grid(row=0)
        self.separator.grid(row=1, sticky="EW")
        self.label.grid(row=2)

        self.text = text

        if grid:
            self.grid(grid)
        elif pack:
            self.pack(pack)

    def pack(self, kwargs):
        self.frame.pack(kwargs)

    def grid(self, kwargs):
        self.frame.grid(kwargs, sticky="S", padx=4, pady=4)

    def get_update_text(self):
        return self.text

    def update(self):
        update_text = self.get_update_text()
        self.set(update_text)

    def get(self):
        return self.value["text"]

    def set(self, text):
        self.value.config(text=text)


class CharacterSheet:

    def __init__(self, window):
        self.master = window
        window.title("Character Sheet")

        self.updatables = {}

        self.load()

        self.create_title()
        self.create_tab_manager()
        self.create_front_page()

        # Move window to centre

        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()
        position_right = int(window.winfo_screenwidth() / 5) - windowWidth
        position_down = int(window.winfo_screenheight() / 5) - windowHeight
        window.geometry(f"+{position_right}+{position_down}")

    # Utility Functions

    def save(self):
        pass

    def load(self):
        char.load()
        self.update()

    def refresh(self):
        pass

    def exit(self):
        self.master.destroy()

    def update(self):
        for ID, object in self.updatables.items():

            try:
                object.update()
            except AttributeError:
                print(f"Error updating {ID} as it has no update method.")

        if hasattr(self, "tab_manager"):
            self.resize_tabs()

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

        self.info_section().grid(row=0, column=0, pady=4, padx=4)
        self.scores_section().grid(row=0, column=1, pady=4, padx=4)
        self.saves_section().grid(row=0, column=2, pady=4, padx=4)
        self.front_page_frame.pack(fill="both", expand=True)

    def info_section(self):
        self.info_frame = tk.Frame(self.front_page_frame,
                                   relief=tk.GROOVE,
                                   borderwidth=2)

        info_frame_rows = {0: tk.Frame(self.info_frame),
                           1: tk.Frame(self.info_frame),
                           2: tk.Frame(self.info_frame),
                           3: tk.Frame(self.info_frame),
                           }

        for row, frame in info_frame_rows.items():
            frame.grid(row=row, sticky="EW")
            for n in range(3):
                frame.grid_columnconfigure(3, weight=1)

        class SimpleInfo(Info_Value_Pair):
            def __init__(self, label_text, row, column, lookup_string, *options):
                options = dict(*options)

                super().__init__(info_frame_rows[row],
                                 label_text,
                                 grid=dict(row=0, column=column),
                                 **options)
                self.lookup_string = lookup_string
                self.update()

            def get_update_text(self):
                (lookup, invalids), = self.lookup_string.items()

                string_list = lookup.split(".", maxsplit=1)

                value = getattr(eval(string_list[0]), string_list[1])

                if invalids and value in invalids:
                    value = ""
                return value

        class CompositeInfo:
            class AlignmentInfo(Info_Value_Pair):
                def __init__(self, label_text, row, column, lookup_strings, *options):
                    options = dict(*options)

                    super().__init__(info_frame_rows[row],
                                     label_text,
                                     grid=dict(row=0, column=column),
                                     **options)
                    self.lookup_strings = lookup_strings
                    self.update()

                def get_update_text(self):
                    output_value = []

                    for lookup, inv in self.lookup_strings.items():

                        string = lookup.split(".", maxsplit=1)
                        value = getattr(eval(string[0]), string[1])

                        if inv and value in inv:
                            value = ""
                        output_value.append(value)
                    return " ".join(output_value)

            class RaceInfo(Info_Value_Pair):
                def __init__(self, label_text, row, column, lookup_strings, *options):
                    options = dict(*options)

                    super().__init__(info_frame_rows[row],
                                     label_text,
                                     grid=dict(row=0, column=column),
                                     **options)
                    self.lookup_strings = lookup_strings
                    self.update()

                def get_update_text(self):
                    output_value = []

                    for lookup, inv in self.lookup_strings.items():

                        string = lookup.split(".", maxsplit=1)
                        value = getattr(eval(string[0]), string[1])

                        if inv and value in inv:
                            value = ""
                        elif string[1] == "subrace":
                            value = f"({value})"

                        output_value.append(value)
                    return " ".join(output_value)

        class ComplexInfo:
            class LevelInfo(Info_Value_Pair):
                def __init__(self, label_text, row, column, null, *options):
                    options = dict(*options)

                    super().__init__(info_frame_rows[row],
                                     label_text,
                                     grid=dict(row=0, column=column),
                                     **options)
                    self.update()

                def get_update_text(self):
                    return ""

            class SizeInfo(Info_Value_Pair):
                def __init__(self, label_text, row, column, null, *options):
                    options = dict(*options)

                    super().__init__(info_frame_rows[row],
                                     label_text,
                                     grid=dict(row=0, column=column),
                                     **options)
                    self.update()

                def get_update_text(self):
                    try:
                        return char.current_size
                    except AttributeError:
                        race_name = char.race

                        return {race.race_name: race.size for race in races.Race.__subclasses__()}[race_name]

            class SpeedInfo(Info_Value_Pair):
                def __init__(self, label_text, row, column, null, *options):
                    options = dict(*options)

                    super().__init__(info_frame_rows[row],
                                     label_text,
                                     grid=dict(row=0, column=column),
                                     **options)
                    self.update()

                def get_update_text(self):
                    try:
                        return str(char.current_speed) + " ft."
                    except AttributeError:
                        race_name = char.race

                        return str(
                            {race.race_name: race.speed for race in races.Race.__subclasses__()}[race_name]) + " ft."

        info_widgets = ((SimpleInfo, "Name", 0, {"char.name": None}, dict(text_font_mod=" 12 bold")),
                        (SimpleInfo, "Age", 2, {"char.age": None}),
                        (CompositeInfo.RaceInfo, "Race", 0, {"char.race": None,
                                                             "char.subrace": "Choose subrace: "}),
                        (CompositeInfo.AlignmentInfo, "Alignment", 1, {"char.ethics": None,
                                                                       "char.morality": None}),
                        (SimpleInfo, "Background", 1, {"char.background": None}),
                        (ComplexInfo.LevelInfo, "Level", 0, {}),
                        (SimpleInfo, "Faith", 1, {"char.faith": None}),
                        (ComplexInfo.SizeInfo, "Size", 1, {}),
                        (ComplexInfo.SpeedInfo, "Speed", 1, {}),
                        (SimpleInfo, "Skin", 2, {"char.skin colour": None}),
                        (SimpleInfo, "Hair", 2, {"char.hair colour": None}),
                        (SimpleInfo, "Eyes", 2, {"char.eye colour": None}),
                        (SimpleInfo, "Height", 2, {"char.height": None}),
                        (SimpleInfo, "Weight", 2, {"char.weight": None}),
                        # (SimpleInfo, "Build", 2, {"char.build": None}),
                        (SimpleInfo, "Age", 2, {"char.age": None}),
                        (SimpleInfo, "Gender", 2, {"char.gender": None}),
                        )

        dict_column_vals = {key: 0 for key in info_frame_rows.keys()}

        def add_info_widget(widget_object, label_text, row, value_lookup, *others):

            widget_name = label_text

            widget_ref = F"info_widget_{widget_name}"

            widget_column = dict_column_vals[row]

            info_widget = widget_object(widget_name, row, widget_column, value_lookup, *others)

            self.updatables[widget_ref] = info_widget

            dict_column_vals[row] += 1

        for widget in info_widgets:
            add_info_widget(*widget)

        for row, frame in info_frame_rows.items():
            for n in range(frame.grid_size()[0]):
                frame.grid_columnconfigure(n, weight=1)

        return self.info_frame

    def scores_section(self):

        self.scores_frame = tk.Frame(self.front_page_frame,
                                     relief=tk.GROOVE,
                                     borderwidth=2)

        tk.Label(self.scores_frame,
                 text="Ability Scores",
                 font=default_font + " 10 bold").grid(row=0, columnspan=6)

        class AbilityScoreRaw:
            def __init__(self, master_frame, name, column):
                self.name = name.lower()
                self.button = tk.Button(master_frame,
                                        font=default_font + " 10",
                                        relief=tk.FLAT,
                                        width=2,
                                        height=1,
                                        anchor=tk.CENTER)
                self.button.grid(row=4, column=column, padx=4)

                self.update()

            def update(self):
                val = getattr(char, f"asi final choice {self.name}")
                self.button.config(text=val)  # TODO: other conditions and variables
                self.score_val = int(val)

        class AbilityScoreMod:
            def __init__(self, master_frame, name, column, score_raw):
                self.name = name.lower()
                self.label = tk.Label(master_frame,
                                      font=default_font + " 12",
                                      width=2,
                                      height=1,
                                      anchor=tk.CENTER)
                self.label.grid(row=2, column=column, padx=4)
                self.score_raw = score_raw
                self.update()

            def format_value(self, val):
                val = int((val - 10) / 2)
                return f"{val:+}"

            def update(self):
                self.score_raw.update()
                self.label.config(text=self.format_value(score_raw.score_val))

        self.ability_scores_raw = {}

        for n, attr in enumerate(glossary.attrs):
            tk.Label(self.scores_frame,
                     text=attr,
                     font=default_font + " 10 bold").grid(row=1, column=n, padx=4)

            object_name = f"ability_score_raw_{attr.lower()}"

            score_raw = AbilityScoreRaw(self.scores_frame, attr, n)

            ttk.Separator(self.scores_frame, orient=tk.HORIZONTAL).grid(row=3, column=n, columnspan=1, sticky="ew")

            score_mod = AbilityScoreMod(self.scores_frame, attr, n, score_raw)

            self.ability_scores_raw[attr] = score_raw

            self.updatables[object_name] = score_raw

        return self.scores_frame

    def saves_section(self):

        self.saves_frame = tk.Frame(self.front_page_frame,
                                    relief=tk.GROOVE,
                                    borderwidth=2)

        tk.Label(self.saves_frame,
                 text="Saving Throws",
                 font=default_font + " 10 bold").pack()

        return self.saves_frame


if __name__ == "__main__":
    char = Character()

    window = tk.Tk()
    CharacterSheet(window)

    style = ttk.Style(window)
    style.configure('TNotebook', tabposition='n')

    # style.map('TCombobox', fieldbackground=[('readonly', 'white')])
    # style.map('TCombobox', selectbackground=[('readonly', 'white')])
    # style.map('TCombobox', selectforeground=[('readonly', 'black')])
    # style.map('TCombobox', selectborderwidth=[('readonly', '0')])

    window.mainloop()
