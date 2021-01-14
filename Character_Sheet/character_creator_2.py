import pickle
import tkinter as tk
from functools import partial
from tkinter import filedialog
from tkinter import ttk

import Character_Sheet.reference.glossary as glossary
import Character_Sheet.reference.races as races
import Character_Sheet.reference.classes as classes
import Character_Sheet.helpers as helpers

default_font = "Verdana"


def export_data(character):
    name = character["Name"]

    if name == "":
        name = "Empty_Character"

    loc = f'saves/{name}'

    with open(loc + '.pkl', "wb") as file:
        pickle.dump(character, file, pickle.HIGHEST_PROTOCOL)
    file.close()


def import_info(filename):
    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()
    return info


def label_entry_pair(master, label_text, textvar, font_mod=" 8", pack=False):
    label = tk.Label(master,
                     text=label_text,
                     font=default_font + font_mod)
    entry = tk.Entry(master,
                     width=24,
                     justify="center",
                     textvariable=textvar)

    if pack:
        label.pack()
        entry.pack()

    return label, entry


def label_values_pair(master, label_text, textvar, font_mod=" 8", pack=True, wrap=False):
    frame = tk.Frame(master)
    label = tk.Label(frame,
                     text=label_text,
                     font=default_font + font_mod + " italic")
    text = tk.Label(frame,
                    textvariable=textvar,
                    font=default_font + font_mod)

    if wrap:
        text['wraplength'] = wrap

    label.pack()
    text.pack()

    if pack:
        frame.pack(pady=4)

    return frame, label, text


class AspectTypes:
    info = "info"
    skill = "skill"
    language = "language"
    asi = "asi"
    feat = "feat"
    race_feature_choice = "race feature choice"
    prof = "proficiency"
    equipment = "equipment"


class Tabs:
    info = "info"
    race = "race"
    class_ = "class"
    background = "background"


class ValueChooserGenerator:
    def __init__(self, character, master, num_choosers, variable_name, value_tab, value_type,
                 invalid_options=[], default_value="", values=[], label={}, grid={}, check_global=False,
                 aspect_order=1):
        char = character
        master_frame = master

        self.frame = tk.Frame(master_frame)
        self.variables = []
        self.widgets = []
        self.aspects = []
        self.value_type = value_type
        self.values = values
        self.default_value = default_value
        self.invalid_options = invalid_options
        self.grid = grid

        if label:
            self.label = tk.Label(self.frame, label)
            self.label_text = tk.StringVar()
            self.label_text.set(self.label['text'])
            self.label["textvariable"] = self.label_text

            self.label.pack()

        for i in range(num_choosers):
            variable = tk.StringVar()
            self.variables.append(variable)
            chooser = ttk.Combobox(self.frame,
                                   textvariable=variable,
                                   state="readonly",
                                   width=16,
                                   font=default_font + " 8",
                                   postcommand=partial(self.checker, i, char.aspects, check_global)
                                   )

            if default_value:
                chooser.set(default_value)

            chooser.pack()

            self.widgets.append(chooser)

            if num_choosers > 1:
                aspect_variable_name = f'{variable_name} {i}'
            else:
                aspect_variable_name = variable_name

            Aspect(aspect_variable_name, value_tab, value_type, variable, chooser, aspect_order, False).add(char)

            self.aspects.append(char.aspects[aspect_variable_name])

        if grid:
            self.frame.grid(grid)
            self.frame.grid_forget()

    def checker(self, index, aspects_list, check_global):

        chosen_local = self.invalid_options.copy()

        if len(self.widgets) > 1:
            for n, widget in enumerate(self.widgets):
                if n != index:
                    chosen_local.append(self.variables[n].get())

        chosen_global = []

        if check_global:
            for aspect in aspects_list.values():
                if aspect.type == self.value_type and aspect.active == True:
                    if len(self.widgets) > 1 or self.aspects[index] != aspect:
                        chosen_global.append(aspect.variable.get())

        chosen_all = chosen_local + chosen_global

        self.widgets[index]['values'] = [value for value in self.values if value not in chosen_all]

    def activate(self, num=None):

        for n, widget in enumerate(self.widgets):

            if widget.get() != self.default_value and widget.get() not in self.values:
                widget.set(self.default_value)

            self.aspects[n].active = False
            widget.pack_forget()
            if (num and n + 1 <= num) or not num:
                widget.pack(pady=1)
                self.aspects[n].active = True

        if self.grid:
            self.frame.grid(self.grid)
        else:
            self.frame.pack(pady=1)

    def deactivate(self):

        if self.grid:
            self.frame.grid_forget()
        else:
            self.frame.pack_forget()

        for n, widget in enumerate(self.widgets):
            self.aspects[n].active = False
            widget.pack_forget()

    def activate_only(self, num=None):
        for n, widget in enumerate(self.widgets):
            self.aspects[n].active = False
            if (num and n + 1 <= num) or not num:
                self.aspects[n].active = True

    def deactivate_only(self):
        for n, widget in enumerate(self.widgets):
            self.aspects[n].active = False


class Aspect:
    def __init__(self, aspect_id, aspect_tab, aspect_type, variable, widget, order, active):
        self.id = aspect_id
        self.tab = aspect_tab
        self.type = aspect_type
        self.variable = variable
        self.widget = widget
        self.order = order
        self.active = active

    def add(self, character):
        character.aspects[self.id] = self

    def update(self, character):
        pass


class CharacterCreator:

    def save(self):

        character_export_dict = {}

        for aspect_id, aspect in self.aspects.items():
            if aspect.active:
                # Currently only works for individual values for get(), will need to adjust.
                character_export_dict[aspect_id] = (aspect.variable.get())

        export_data(character_export_dict)

        print("Save successful!")

    def load(self):

        filename = tk.filedialog.askopenfilename(initialdir="saves/",
                                                 title="Select save file",
                                                 filetypes=(
                                                     ("Pickled Files", "*.pkl"),
                                                     ("all files", "*.*")))

        character_import_dict = import_info(filename)
        num_layers = max([aspect.order for aspect in self.aspects.values()]) + 1
        for condition in range(num_layers):
            for key, value in character_import_dict.items():
                try:
                    aspect = self.aspects[key]

                    if aspect.order == condition:
                        aspect.variable.set(value)
                        aspect.active = True
                except:
                    print(f"Error loading {key} value")

    def exit(self):

        def exit_save_and_close():
            exit_window.destroy()
            self.save()
            window.destroy()

        def exit_close():
            exit_window.destroy()
            window.destroy()

        exit_window = tk.Tk()
        exit_label = tk.Label(exit_window, text="Would you like to save?",
                              font=default_font + " 10")
        exit_label.pack()
        exit_buttons = tk.Frame(exit_window)
        yes_button = tk.Button(exit_buttons, width=8, text="Yes",
                               command=exit_save_and_close)
        no_button = tk.Button(exit_buttons, width=8, text="No", command=exit_close)
        cancel_button = tk.Button(exit_buttons, width=8, text="Cancel",
                                  command=exit_window.destroy)

        yes_button.grid(row=1, column=0, padx=4)
        no_button.grid(row=1, column=1, padx=4, pady=8)
        cancel_button.grid(row=1, column=2, padx=4)

        exit_buttons.pack()

    def sanitise(self):
        print([aspect.order for aspect in self.aspects.values()])
        # character_export_dict = {}
        #
        # for aspect_id, aspect in self.aspects.items():
        #     print(aspect_id, aspect.variable.get(), aspect.active)
        #
        #     # if aspect.active:
        #     #     character_export_dict[aspect_id] = (aspect.variable.get())
        #
        # # export_data(character_export_dict)

    def reset_tab_aspects(self, tab_hash):

        for aspect in self.aspects.values():
            if aspect.tab is tab_hash:
                aspect.active = False

    def create_title(self):
        self.title = tk.Label(self.master,
                              text='Character Creator',
                              bd=8,
                              font=default_font + " 14 bold")

        self.title.pack(side=tk.TOP)

        self.main_menu = tk.Menu(self.master)

        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_command(label="Sanitise", command=self.sanitise)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.main_menu)

    def create_tab_manager(self):

        self.tab_manager = ttk.Notebook(self.master)

        self.info_tab = ttk.Frame(self.tab_manager,
                                  relief=tk.FLAT,
                                  borderwidth=5)
        self.race_tab = ttk.Frame(self.tab_manager,
                                  relief=tk.FLAT,
                                  borderwidth=5)
        self.class_tab = ttk.Frame(self.tab_manager,
                                   relief=tk.FLAT,
                                   borderwidth=5)
        self.background_tab = ttk.Frame(self.tab_manager,
                                        relief=tk.FLAT,
                                        borderwidth=5)

        self.tab_manager.add(self.info_tab, text="Info")
        self.tab_manager.add(self.race_tab, text="Race")
        self.tab_manager.add(self.class_tab, text="Class")
        self.tab_manager.add(self.background_tab, text="Background")

        self.tab_manager.bind("<<NotebookTabChanged>>", self.changed_tabs)

        self.tab_manager.pack()

    def create_info_tab(self):

        def name_frame_config():
            name_frame = tk.Frame(self.info_frame)
            character_name = tk.StringVar()
            name_label, name_entry = label_entry_pair(name_frame, "Character Name", character_name, " 12 bold", True)
            name_entry.config(width=24,
                              justify="center")

            Aspect("Name", Tabs.info, AspectTypes.info, character_name, name_entry, 0, True).add(self)

            name_frame.pack(padx=8, pady=(8, 16))

        def data_frame_config():

            data_frame = tk.Frame(self.info_frame)

            # Age

            age_frame = tk.Frame(data_frame)
            character_age = tk.StringVar()
            age_label, age_entry = label_entry_pair(age_frame, "Age", character_age, " 10 bold", False)
            age_label.grid(row=0)
            age_entry.grid(row=1)

            age_entry.config(width=8,
                             justify="center")
            Aspect("Age", Tabs.info, AspectTypes.info, character_age, age_entry, 1, True).add(self)

            # Gender

            gender_frame = tk.Frame(data_frame)
            character_gender = tk.StringVar()
            gender_label, gender_entry = label_entry_pair(gender_frame, "Gender", character_gender, " 10 bold", False)
            gender_label.grid(row=0)
            gender_entry.grid(row=1)
            gender_entry.config(width=8,
                                justify="center")
            Aspect("Gender", Tabs.info, AspectTypes.info, character_gender, gender_entry, 1, True).add(self)

            # Physical Attributes

            appearance_frame = tk.Frame(data_frame)
            size_frame = tk.Frame(data_frame)

            appearance_aspects = ["Skin Colour",
                                  "Hair Colour",
                                  "Eye Colour"]
            size_aspects = ["Height",
                            "Weight",
                            "Build"]

            for j in range(len(appearance_aspects)):

                frames = appearance_frame, size_frame
                aspects = appearance_aspects, size_aspects

                for k, frame in enumerate(frames):
                    aspect_var = tk.StringVar()
                    label, entry = label_entry_pair(frame, aspects[k][j], aspect_var, " 10 bold", False)
                    entry.config(width=10,
                                 justify="center")

                    label.grid(row=1, column=j, pady=(2, 1), padx=4)
                    entry.grid(row=2, column=j, padx=8)

                    Aspect(aspects[k][j], Tabs.info, AspectTypes.info, aspect_var, entry, 1, True).add(self)

            age_frame.grid(row=0, column=0, padx=(0, 4), sticky="E")
            gender_frame.grid(row=0, column=1, padx=(4, 0), sticky="W")
            appearance_frame.grid(row=1, column=0, columnspan=2, padx=(0, 8))
            size_frame.grid(row=2, column=0, columnspan=2, padx=(8, 0))

            data_frame.pack()

        def faith_frame_config():
            faith_frame = tk.Frame(self.info_frame)

            character_faith = tk.StringVar()

            faith_label, faith_entry = label_entry_pair(faith_frame, "Faith", character_faith, " 10 bold", True)
            faith_entry.config(width=16,
                               justify="center")

            Aspect("Faith", Tabs.info, AspectTypes.info, character_faith, faith_entry, 1, True).add(self)

            faith_frame.pack(pady=2)

        def alignment_frame_config():

            alignment_frame = tk.Frame(self.info_frame)

            alignment_label = tk.Label(alignment_frame,
                                       text='Alignment',
                                       font=default_font + " 10 bold")
            character_ethics = tk.StringVar()
            character_morality = tk.StringVar()
            ethics = ttk.Combobox(alignment_frame,
                                  values=["Lawful", "Neutral", "Chaotic"],
                                  state="readonly",
                                  textvariable=character_ethics,
                                  width=8,
                                  justify="center")
            morality = ttk.Combobox(alignment_frame,
                                    values=["Good", "Neutral", "Evil"],
                                    state="readonly",
                                    textvariable=character_morality,
                                    width=8,
                                    justify="center")

            Aspect("Ethics", Tabs.info, AspectTypes.info, character_ethics, ethics, 1, True).add(self)
            Aspect("Morality", Tabs.info, AspectTypes.info, character_morality, morality, 1, True).add(self)

            alignment_label.grid(row=0, columnspan=2)
            ethics.grid(row=1, column=0, padx=(0, 2))
            morality.grid(row=1, column=1, padx=(2, 0))

            alignment_frame.pack(pady=(2, 8))

        self.reset_tab_aspects(Tabs.info)

        self.info_frame = tk.Frame(self.info_tab,
                                   relief=tk.SUNKEN,
                                   borderwidth=4,
                                   )
        name_frame_config()
        data_frame_config()
        faith_frame_config()
        alignment_frame_config()

        self.info_frame.pack(fill="both", expand=True)

    def create_race_tab(self):

        """Can do Tasha's optionals in the future"""
        """https://thetrove.is/Books/Dungeons%20%26%20Dragons%20%5Bmulti%5D/5th%20Edition%20%285e%29/Core/Tasha%E2%80%99s%20Cauldron%20of%20Everything%20%28HQ%2C%20Both%20Covers%29.pdf"""

        def race_choice_config():

            self.character_race = tk.StringVar()

            self.race_chooser = ttk.Combobox(self.race_frame,
                                             values=sorted([race for race in races.race_list]),
                                             state="readonly",
                                             width=16,
                                             textvariable=self.character_race,
                                             justify="center")

            Aspect("Race", Tabs.race, AspectTypes.info, self.character_race, self.race_chooser, 0, True).add(self)

            self.race_choice_prompt = "Choose race: "
            self.race_chooser.set(self.race_choice_prompt)

            self.character_race.trace_add('write', race_changed)

            self.race_chooser.grid(row=1, columnspan=3, pady=2)

        def race_changed(*args):

            if self.character_race.get() != self.race_choice_prompt:

                self.race_instance = races.race_list[self.character_race.get()]

                if self.race_instance.__subclasses__():

                    self.subrace_chooser.grid(row=2, columnspan=3, pady=2)
                    subraces_list = [subrace.subrace_name for subrace in self.race_instance.__subclasses__()]
                    if self.character_subrace.get() not in subraces_list:
                        self.character_subrace.trace_remove('write', self.character_subrace.trace_info()[0][1])
                        self.character_subrace.set("Choose subrace: ")
                        self.subrace_instance = None
                        self.character_subrace.trace_add('write', subrace_changed)

                else:
                    self.subrace_chooser.grid_forget()
                    self.character_subrace.trace_remove('write', self.character_subrace.trace_info()[0][1])
                    self.character_subrace.set("Choose subrace: ")
                    self.character_subrace.trace_add('write', subrace_changed)

                pack_race_info()
                self.resize_tabs()

                feature_constructor(self.race_instance)

            else:

                self.race_asi_choice.deactivate()
                self.character_race_language.deactivate()

                self.subrace_chooser.grid_forget()
                self.character_subrace.trace_remove('write', self.character_subrace.trace_info()[0][1])
                self.character_subrace.set("Choose subrace: ")
                self.character_subrace.trace_add('write', subrace_changed)
                self.race_info_frame.grid_forget()
                self.asi_frame.grid_forget()
                self.bottom_divider.grid_forget()
                self.divider_2.grid_forget()
                self.racial_features_frame.grid_forget()

                self.resize_tabs()
                self.master.update()
                self.tab_manager.config(width=self.master.winfo_width())

        def subrace_choice_config():

            self.character_subrace = tk.StringVar()

            self.subrace_chooser = ttk.Combobox(self.race_frame,
                                                values=[],
                                                postcommand=get_subclasses,
                                                state="readonly",
                                                width=16,
                                                textvariable=self.character_subrace,
                                                justify="center")

            Aspect("Subrace", Tabs.race, AspectTypes.info, self.character_subrace, self.subrace_chooser, 0,
                   True).add(self)

            self.subrace_choice_prompt = "Choose subrace: "
            self.subrace_chooser.set(self.subrace_choice_prompt)

            self.character_subrace.trace_add('write', subrace_changed)

        def get_subclasses():
            subraces_list = [subrace.subrace_name for subrace in self.race_instance.__subclasses__()]
            self.subrace_chooser['values'] = subraces_list

        def subrace_changed(*args):

            if self.character_subrace.get() != self.subrace_choice_prompt:
                self.subrace_instance = \
                    {subrace.subrace_name: subrace for subrace in self.race_instance.__subclasses__()}[
                        self.character_subrace.get()]

                feature_constructor(self.subrace_instance)

        def feature_constructor(instance):

            if instance not in races.Race.__subclasses__():
                is_subrace = True
            else:
                is_subrace = False

            if hasattr(instance, "ASI"):
                self.asi_frame.grid_forget()
                self.asi_attributes_frame.grid_forget()
                self.race_asi_choice.deactivate()
                pack_race_asi(instance, is_subrace)
            else:
                self.asi_frame.grid_forget()
                self.asi_attributes_frame.grid_forget()
                self.race_asi_choice.deactivate()

            if hasattr(instance, "languages"):
                pack_race_languages(instance)

            if hasattr(instance, "features"):
                pack_other_features(instance, is_subrace)

            self.resize_tabs()

        def race_info_config():

            self.race_info_frame = tk.Frame(self.race_frame)

            race_info_label = tk.Label(self.race_info_frame,
                                       text="Racial Stats:",
                                       font=default_font + " 10 bold")

            self.race_size_text = tk.StringVar()
            self.race_speed_text = tk.StringVar()
            self.race_language_text = tk.StringVar()

            self.race_size_text.set("Medium")
            self.race_speed_text.set(f'{30} ft.')
            self.race_language_text.set("Common")

            self.race_base_info = tk.Frame(self.race_info_frame)
            race_size_label = tk.Label(self.race_base_info,
                                       text="Size",
                                       font=default_font + " 10 bold")
            race_speed_label = tk.Label(self.race_base_info,
                                        text="Speed",
                                        font=default_font + " 10 bold")
            divider = ttk.Separator(self.race_base_info,
                                    orient=tk.VERTICAL)

            race_size_value = tk.Label(self.race_base_info,
                                       textvariable=self.race_size_text,
                                       font=default_font + " 10")

            race_speed_value = tk.Label(self.race_base_info,
                                        textvariable=self.race_speed_text,
                                        font=default_font + " 10")

            race_languages_label = tk.Label(self.race_base_info,
                                            text="Languages",
                                            font=default_font + " 10 bold")

            race_languages_value = tk.Label(self.race_base_info,
                                            textvariable=self.race_language_text,
                                            font=default_font + " 10",
                                            justify=tk.LEFT)

            self.character_race_language = ValueChooserGenerator(character=self,
                                                                 master=self.race_base_info,
                                                                 num_choosers=1,
                                                                 variable_name="Race Language",
                                                                 values=["None"] + glossary.all_languages,
                                                                 value_tab=Tabs.race,
                                                                 value_type=AspectTypes.language,
                                                                 default_value="Choose language: ",
                                                                 grid=dict(row=3, column=2, sticky="NW"),
                                                                 check_global=True)

            race_size_label.grid(row=0, column=0, sticky="E")
            race_size_value.grid(row=0, column=2, sticky="W")
            race_speed_label.grid(row=1, column=0, sticky="E")
            race_speed_value.grid(row=1, column=2, sticky="W")
            race_languages_label.grid(row=2, column=0, sticky="NE")
            race_languages_value.grid(row=2, column=2, sticky="NW")

            divider.grid(column=1, row=0, rowspan=5, sticky="NS")

            self.bottom_divider = ttk.Separator(self.race_base_info)

            race_info_label.grid(row=0)
            self.race_base_info.grid(row=1, column=0, sticky="N")

        def pack_race_info():
            self.race_info_frame.grid(row=3, column=0, sticky="N", padx=4)

            self.race_size_text.set(self.race_instance.size)
            self.race_speed_text.set(f'{self.race_instance.speed} ft.')

        def race_asi_config():

            self.asi_frame = tk.Frame(self.race_info_frame)

            asi_label = tk.Label(self.asi_frame,
                                 text="Ability score increases:",
                                 font=default_font + " 10 bold")

            asi_label.grid(row=0, sticky="N")

            self.asi_attributes_frame = tk.Frame(self.asi_frame)

            self.asi_automatic_values = [None] * 6
            for n, attribute in enumerate(glossary.attrs):
                label = tk.Label(self.asi_attributes_frame,
                                 text=attribute,
                                 font=default_font + " 10 bold")
                label.grid(row=n, column=0, sticky="E")

                value = tk.Label(self.asi_attributes_frame,
                                 font=default_font + " 10")

                value.grid(row=n, column=2, sticky="W")
                self.asi_automatic_values[n] = value

            ttk.Separator(self.asi_attributes_frame,
                          orient=tk.VERTICAL).grid(column=1, row=0, sticky="NS",
                                                   rowspan=
                                                   self.asi_attributes_frame.grid_size()[1])

            self.asi_choice_text = tk.StringVar()

            self.race_asi_choice = ValueChooserGenerator(character=self,
                                                         master=self.asi_frame,
                                                         num_choosers=2,
                                                         variable_name="Race ASI",
                                                         value_tab=Tabs.race,
                                                         value_type=AspectTypes.asi,
                                                         grid=dict(row=2, sticky=tk.N),
                                                         check_global=False,
                                                         label=dict(textvariable=self.asi_choice_text,
                                                                    font=default_font + " 8"))

        def pack_race_languages(instance):

            default_languages = []

            num_language_choice = 0

            for lang in instance.languages:
                if isinstance(lang, str):
                    default_languages.append(lang)
                else:
                    num_language_choice += 1

            self.race_language_text.set("\n".join(default_languages))

            if num_language_choice:
                self.character_race_language.activate(num_language_choice)
                self.character_race_language.invalid_options = default_languages
            else:
                self.character_race_language.deactivate()

        def pack_race_asi(instance, is_subrace):

            for asi in self.asi_automatic_values:
                asi['text'] = ""

            self.asi_frame.grid(row=2, column=0)
            self.bottom_divider.grid(column=0, row=5, columnspan=3, sticky="EW", pady=(4, 0))

            try:
                asi_list = list(instance.ASI)
            except Exception as e:
                print(e)

            all_asi = asi_list

            if is_subrace:
                if hasattr(self.race_instance, "ASI"):
                    all_asi += list(self.race_instance.ASI)

            asi_choice = False

            for asi in all_asi:
                if isinstance(asi[0], list):
                    asi_choice = asi[1]
                    asi_choice_options = asi[0]
                    if asi[1] <= 1:
                        self.race_asi_choice.label_text.set("Choose ability score to increase by +1:")
                    elif asi[1] > 1:
                        self.race_asi_choice.label_text.set("Choose ability scores to increase by +1:")

                else:
                    self.asi_attributes_frame.grid(row=1)
                    attr_index = (glossary.attrs.index(asi[0].__name__))
                    self.asi_automatic_values[attr_index].configure(text=f'{asi[1]:+d}')

            if asi_choice:
                self.race_asi_choice.activate(asi_choice)
                self.race_asi_choice.values = [attr.__name__ for attr in asi_choice_options]
            else:
                self.race_asi_choice.deactivate()

        def race_other_features_config():

            self.divider_2 = ttk.Separator(self.race_frame, orient=tk.VERTICAL)

            self.racial_features_frame = tk.Frame(self.race_frame)

            self.race_features_title = tk.Label(self.racial_features_frame,
                                                text="Racial Features:",
                                                font=default_font + " 10 bold",
                                                anchor="n")

            # Race Frames
            self.race_features_frame = tk.Frame(self.racial_features_frame)
            self.race_features_label = tk.Label(self.race_features_frame,
                                                text="Race Features:",
                                                font=default_font + " 8 bold",
                                                anchor="n")
            self.race_chooser_features_frame = tk.Frame(self.race_features_frame)
            self.race_general_features_frame = tk.Frame(self.race_features_frame)

            # Subrace Frames
            self.subrace_features_frame = tk.Frame(self.racial_features_frame)
            self.subrace_features_label = tk.Label(self.subrace_features_frame,
                                                   text="Subrace Features:",
                                                   font=default_font + " 8 bold",
                                                   anchor="n")
            self.subrace_chooser_features_frame = tk.Frame(self.subrace_features_frame)
            self.subrace_general_features_frame = tk.Frame(self.subrace_features_frame)

            self.race_features_title.grid(row=0)

            self.race_features_label.grid(row=0)
            self.race_chooser_features_frame.grid(row=1)
            self.race_general_features_frame.grid(row=2)

            self.subrace_features_label.grid(row=0)
            self.subrace_chooser_features_frame.grid(row=1)
            self.subrace_general_features_frame.grid(row=2)

        class FeatureWidgets:
            def __init__(self, char):
                self.char = char

            def chooser(self, aspect_name, feature_frame, feature_values):
                # print("Packing chooser", aspect_name)

                values = feature_values.keys()

                default = f"Choose {aspect_name[0]} feature:"

                chooser = ValueChooserGenerator(character=self.char,
                                                master=feature_frame,
                                                num_choosers=1,
                                                variable_name=" ".join(aspect_name),
                                                value_tab=Tabs.race,
                                                value_type=AspectTypes.race_feature_choice,
                                                default_value=default,
                                                values=values,
                                                check_global=True
                                                )
                chooser.widgets[0]["width"] = 20

                chooser.activate()
                chooser.deactivate_only()

                self.char.race_feature_widgets["activatable"].append(chooser)

                return chooser

            def other(self, feature_name, feature_frame, feature_values):
                widget = tk.Label(feature_frame,
                                  text=f'{feature_values.desc}',
                                  wraplength=400,
                                  justify=tk.LEFT,
                                  anchor="w",
                                  font=default_font + " 8"
                                  )
                widget.pack(side=tk.LEFT)

                return widget

            def skill(self, aspect_name, feature_frame, feature_values):
                num_choosers = len(feature_values)
                values = feature_values[0]
                widget = ValueChooserGenerator(character=self.char,
                                               master=feature_frame,
                                               num_choosers=num_choosers,
                                               variable_name=" ".join(aspect_name),
                                               value_tab=Tabs.race,
                                               value_type=AspectTypes.skill,
                                               default_value="Choose skill:",
                                               values=values,
                                               aspect_order=2,
                                               check_global=True
                                               )
                widget.activate()
                widget.deactivate_only()

                self.char.race_feature_widgets["activatable"].append(widget)

                return widget

            def feat(self, aspect_name, feature_frame, feature_values):
                num_choosers = len(feature_values)
                values = feature_values[0]

                widget = ValueChooserGenerator(character=self.char,
                                               master=feature_frame,
                                               num_choosers=num_choosers,
                                               variable_name=" ".join(aspect_name),
                                               value_tab=Tabs.race,
                                               value_type=AspectTypes.feat,
                                               default_value="Choose feat:",
                                               values=values,
                                               aspect_order=2,
                                               check_global=True)
                widget.activate()  # Add prereq here
                widget.deactivate_only()

                self.char.race_feature_widgets["activatable"].append(widget)

                return widget

            def prof(self, aspect_name, feature_frame, feature_values):
                prof_type = feature_values[0]
                feature_vals = feature_values[1][0]
                num_choosers = len(feature_values[1])
                variable_name = " ".join(aspect_name + [prof_type])
                widget = ValueChooserGenerator(character=self.char,
                                               master=feature_frame,
                                               num_choosers=num_choosers,
                                               variable_name=variable_name,
                                               value_tab=Tabs.race,
                                               value_type=AspectTypes.prof,
                                               default_value=f"Choose {prof_type} proficiency:",
                                               values=feature_vals,
                                               aspect_order=2,
                                               check_global=True)

                widget.widgets[0]["width"] = len(widget.default_value) - 4

                widget.activate()
                widget.deactivate_only()

                self.char.race_feature_widgets["activatable"].append(widget)

                return widget

        def add_dynamic_aspects():

            def get_feature_info(name, feature_name, feature, origin):

                feature_type = feature[0]

                feature_opts = feature[1]

                return (origin, name, feature_name, feature_type, feature_opts)

            def feature_splitter(feature_list, name, origin):

                features = []

                for feature in feature_list.items():
                    feature_name = feature[0]
                    if not isinstance(feature[1], list):
                        features.append(get_feature_info(name, feature_name, feature[1], origin))
                    else:
                        for feature_set in feature[1]:
                            features.append(get_feature_info(name, feature_name, feature_set, origin))
                return features

            def list_features(name, instance, origin):

                feature_list = []

                if instance.features:
                    feature_list.extend(feature_splitter(instance.features.all, name, origin))
                    # if hasattr(instance, Ftype.choice):
                    #     origin += " choice"
                    #     feature_list.extend(feature_splitter(instance.choice_features, name, origin))

                return feature_list

            from collections import defaultdict

            def deep_dict():
                return defaultdict(deep_dict)

            self.race_features_all = deep_dict()

            Ftype = races.FeatureType

            widgets_set = FeatureWidgets(self)

            feature_switcher = {
                Ftype.choice: widgets_set.chooser,
                Ftype.other: widgets_set.other,
                Ftype.skills: widgets_set.skill,
                Ftype.feats: widgets_set.feat,
                Ftype.proficiencies: widgets_set.prof
            }

            all_features = []

            all_races = [race for race in races.Race.__subclasses__()]
            for race in all_races:
                race_name = race.race_name
                origin = "race"
                all_features.extend(list_features(race_name, race, origin))

                subraces = [subrace for subrace in race.__subclasses__()]
                for subrace in subraces:
                    subrace_name = subrace.subrace_name
                    origin = "subrace"
                    all_features.extend(list_features(race_name + " " + subrace_name, subrace, origin))

            all_features = [feature for feature in all_features if feature is not None]

            top_frames = {'race': self.race_general_features_frame,
                          'subrace': self.subrace_general_features_frame,
                          'race choice': self.race_chooser_features_frame,
                          'subrace choice': self.subrace_chooser_features_frame}

            # Put into master dictionary and structure
            for feature in all_features:
                feature_level, feature_origin, feature_name, feature_type, feature_opts = feature
                self.race_features_all[feature_level][feature_origin][feature_name][feature_type] = feature_opts

            self.race_feature_widgets = {}

            self.race_feature_widgets["activatable"] = []

            for feature_level, feature_origin in self.race_features_all.items():
                top_frame = top_frames[feature_level]

                # print(feature_level)
                for feature_origin, feature_names in feature_origin.items():
                    # print("\t", feature_origin)
                    for feature_name, feature_types in feature_names.items():

                        feature_key = (feature_level, feature_origin, feature_name)

                        # print(feature_key)

                        if Ftype.choice in feature_types.keys():
                            top_frame = top_frames[feature_level + " choice"]

                        if feature_key not in self.race_feature_widgets:
                            feature_frame = tk.Frame(top_frame)
                            feature_label = tk.Label(feature_frame,
                                                     text=feature_name,
                                                     font=default_font + " 8 italic")
                            self.race_feature_widgets[feature_key] = {"frame": feature_frame,
                                                                      "label": feature_label}
                            # feature_frame.pack()
                            feature_label.pack()
                        else:
                            feature_frame = self.race_feature_widgets[feature_key]["frame"]

                        # print("\t\t", feature_name)
                        for feature_type, feature_opts in feature_types.items():

                            aspect_name = [feature_level, feature_origin, feature_name, feature_type]

                            # print("\t\t\t", feature_type)

                            widget = feature_switcher[feature_type](aspect_name, feature_frame, feature_opts)
                            self.race_feature_widgets[feature_key].update({feature_type: widget})

                            if feature_type == Ftype.choice:

                                # Pack options
                                self.race_feature_widgets[feature_key]["choice_widgets"] = {}
                                for opt_name, (opt_type, opt_vals) in feature_opts.items():
                                    opt_frame = tk.Frame(feature_frame)
                                    # opt_label = tk.Label(opt_frame,
                                    #                      text=opt_name,
                                    #                      font=default_font + " 8 italic")
                                    # opt_label.pack()
                                    opt_aspect_name = aspect_name + [opt_name]

                                    opt_widget = feature_switcher[opt_type](opt_aspect_name, opt_frame, opt_vals)

                                    self.race_feature_widgets[feature_key]["choice_widgets"].update(
                                        {opt_name: {'widget': opt_widget,
                                                    'type': opt_type,
                                                    'frame': opt_frame}})

                                # Add trace to variable

                                choice_variable = widget.variables[0]

                                choice_default = widget.default_value

                                change_feature_func = partial(feature_changed, choice_variable,
                                                              self.race_feature_widgets[feature_key]["choice_widgets"],
                                                              choice_default)

                                choice_variable.trace_add("write", change_feature_func)

            # Go through and generate all possible choosers and aspects. When actually packing, call them appropriately. Not nice but it should work.

        def pack_other_features(instance, is_subrace):

            # Cleanup old

            def wipe_clean(frame):
                for child in frame.winfo_children():
                    child.pack_forget()

            top_frames = {'race': self.race_general_features_frame,
                          'subrace': self.subrace_general_features_frame,
                          'race choice': self.race_chooser_features_frame,
                          'subrace choice': self.subrace_chooser_features_frame}

            Ftype = races.FeatureType
            activatable_widgets = [Ftype.choice, Ftype.skills, Ftype.feats, Ftype.proficiencies]

            if not is_subrace:
                frames = top_frames.values()
                features_level = "race"
                features_origin = self.race_instance.race_name
                self.race_features_frame.grid_forget()
                self.subrace_features_frame.grid_forget()


            else:
                frames = [self.subrace_general_features_frame,
                          self.subrace_chooser_features_frame]
                features_level = "subrace"
                features_origin = " ".join([self.race_instance.race_name, self.subrace_instance.subrace_name])
                self.subrace_features_frame.grid_forget()
                levels = ['subrace']
                if not self.race_instance.features:
                    self.race_features_frame.grid_forget()
                    levels.append('race')

            for key, values in self.race_feature_widgets.items():
                if features_level in key:
                    for value, object in values.items():
                        if value in activatable_widgets:
                            object.deactivate_only()

            for frame in frames:
                wipe_clean(frame)
                tk.Frame(frame).pack()

            # Add new

            if instance.features:

                self.divider_2.grid(row=3, column=1, sticky="NS", rowspan=8)
                self.racial_features_frame.grid(row=3, column=2, sticky="N", padx=4)

                if not is_subrace:

                    self.race_features_frame.grid(row=1)

                else:
                    self.subrace_features_frame.grid(row=2)

                for feature_name, feature_values in instance.features.all.items():
                    feature_entry = self.race_feature_widgets[(features_level, features_origin, feature_name)]
                    feature_entry['frame'].pack()

                    for entry, value in feature_entry.items():
                        if entry in activatable_widgets:
                            value.activate_only()

                # print(self.race_feature_widgets.keys())
                # print((features_level, features_origin))

            else:
                self.divider_2.grid_forget()
                self.racial_features_frame.grid_forget()

        def feature_changed(choice, choice_options, default, *args):

            Ftype = races.FeatureType
            activatable_widgets = [Ftype.choice, Ftype.skills, Ftype.feats, Ftype.proficiencies]

            choice_name = choice.get()

            for choice, choice_values in choice_options.items():
                if choice_values['type'] in activatable_widgets:
                    choice_values['widget'].deactivate_only()
                choice_values['frame'].pack_forget()

            if choice_name != default:

                chosen = choice_options[choice_name]

                chosen['frame'].pack()

                if chosen['type'] in activatable_widgets:
                    chosen['widget'].activate_only()

        ### Begin Code

        self.reset_tab_aspects(Tabs.race)

        self.race_frame = tk.Frame(self.race_tab,
                                   relief=tk.SUNKEN,
                                   borderwidth=4,
                                   )

        self.race_label = tk.Label(self.race_frame,
                                   text="Race",
                                   font=default_font + " 12 bold").grid(row=0, columnspan=3, pady=8)

        race_choice_config()
        subrace_choice_config()
        race_info_config()
        race_asi_config()
        race_other_features_config()
        add_dynamic_aspects()

        self.race_frame.pack(fill="both", expand=True)

        self.race_frame.grid_rowconfigure(0, weight=1)
        self.race_frame.grid_columnconfigure(0, weight=1)

    def create_class_tab(self):

        def class_choice_config():
            self.character_class = tk.StringVar()
            self.class_chooser = ttk.Combobox(self.class_frame,
                                              values=sorted(
                                                  [c.class_name for c in classes.CharacterClass.__subclasses__()]),
                                              state="readonly",
                                              width=16,
                                              textvariable=self.character_class,
                                              justify="center")

            Aspect("Class", Tabs.class_, AspectTypes.info, self.character_class, self.class_chooser, 0, True).add(self)

            self.class_choice_prompt = "Choose class: "
            self.class_chooser.set(self.class_choice_prompt)

            self.character_class.trace_add('write', class_changed)

            self.class_chooser.grid(row=1, pady=2)

            self.class_features_frame = tk.Frame(self.class_frame)

            self.left_frame = tk.Frame(self.class_features_frame)
            tk.Label(self.left_frame,
                     text="Class Proficiencies:",
                     font=default_font + " 9 bold").pack()
            self.left_frame.grid(row=1, column=0, sticky="N")

            self.central_frame = tk.Frame(self.class_features_frame)
            tk.Label(self.central_frame,
                     text="Class Something:",
                     font=default_font + " 9 bold").pack()
            self.central_frame.grid(row=1, column=1, sticky="N")

            self.right_frame = tk.Frame(self.class_features_frame)
            tk.Label(self.right_frame,
                     text="Class Equipment:",
                     font=default_font + " 9 bold").pack()
            self.right_frame.grid(row=1, column=2, sticky="N")

        def class_info_config():
            self.class_info_frame = tk.Frame(self.class_features_frame)

            self.class_desc = tk.Label(self.class_info_frame,
                                       wraplength=600,
                                       justify=tk.CENTER,
                                       # anchor="w",
                                       font=default_font + " 8"
                                       )

            self.class_rpgbot = tk.Label(self.class_info_frame,
                                         wraplength=600,
                                         justify=tk.CENTER,
                                         # anchor="w",
                                         font=default_font + " 8"
                                         )

            # tk.Label(self.class_info_frame,
            #          text = "Class Description:",
            #          font=default_font+ " 8 italic").pack()
            self.class_desc.pack()
            tk.Label(self.class_info_frame,
                     text="Class Design:",
                     font=default_font + " 8 italic").pack(pady=(8, 2))
            self.class_rpgbot.pack(pady=(2, 8))

            self.class_info_frame.grid(row=0, columnspan=3)

        def class_stats_config():

            self.class_primary_attr = tk.StringVar()
            frame, self.class_attr_label, text = label_values_pair(self.left_frame, "Primary Attribute:",
                                                                   self.class_primary_attr)

            self.class_hit_die = tk.StringVar()
            label_values_pair(self.left_frame, "Hit Die:", self.class_hit_die)

            self.class_armour_profs = tk.StringVar()
            label_values_pair(self.left_frame, "Armour Proficiencies:", self.class_armour_profs, wrap=200)

            self.class_weapon_profs = tk.StringVar()
            label_values_pair(self.left_frame, "Weapon Proficiencies:", self.class_weapon_profs, wrap=200)

            self.class_tool_profs = tk.StringVar()
            label_values_pair(self.left_frame, "Tool Proficiencies:", self.class_tool_profs, wrap=200)

            self.class_saving_throws = tk.StringVar()
            label_values_pair(self.left_frame, "Saving Throws:", self.class_saving_throws, wrap=200)

        def class_skills_config():

            self.class_skills_chooser = ValueChooserGenerator(character=self,
                                                              master=self.central_frame,
                                                              num_choosers=4,
                                                              variable_name="Class Skill",
                                                              value_tab=Tabs.class_,
                                                              value_type=AspectTypes.skill,
                                                              label=dict(text="Choose skill proficiencies:",
                                                                         font=default_font + " 8"),
                                                              check_global=True)

        def class_equipment_config():

            class EquipmentChooser:

                def __init__(self, char):

                    self.update_size = char.resize_tabs

                    self.char_temp = char

                    self.chooser_frame = tk.Frame(char.right_frame)
                    tk.Label(self.chooser_frame,
                             text="You recieve the following items, plus any provided by your background:",
                             font=default_font + " 8",
                             wraplength=220).pack()
                    self.chooser_internal_frame = tk.Frame(self.chooser_frame)
                    self.chooser_internal_frame.pack(fill="x", expand=True)

                    # tk.Label(self.chooser_frame,
                    #          text="Additionally, you will also receive:",
                    #          font=default_font + " 8").pack()

                    self.end_label = tk.Label(self.chooser_frame,
                                              font=default_font + " 8")

                    self.end_label.pack(anchor=tk.W)

                    self.chooser_frame.pack()  # padx=(0,8))

                    self.selectors = {}

                def selector_packer(self, n_import, choice, variable):

                    frame = tk.Frame(self.chooser_internal_frame)
                    frame.pack(fill="x", expand=True)

                    self.selectors[n_import]["choosers"] = {}

                    self.chooser_frame_dummies = []

                    for n, option in enumerate(choice):

                        c_frame = tk.Frame(frame)

                        rdb = tk.Radiobutton(frame,
                                             variable=variable,
                                             value=n,
                                             command=self.chooser_checker)

                        text = []

                        for item in option:
                            item_value = item[0]
                            item_num = item[1]

                            if not isinstance(item_value, (tuple, list)):
                                if not item_value.__subclasses__():
                                    text.append(item_value.syntax(item_num))
                                else:
                                    """Plot a chooser and get options"""
                                    option_name = item_value.syntax(item_num)
                                    text.append(option_name)
                                    self.chooser_packer((n_import, n), c_frame, item_num, (item_value,))
                            else:
                                option_name = item_value[0].syntax_start(item_num) + " " + \
                                              item_value[1].syntax_end(item_num)
                                text.append(option_name)

                                self.chooser_packer((n_import, n), c_frame, item_num, item_value)

                        true_text = helpers.list_syntax(text).capitalize()
                        rdb.config(text=true_text)
                        rdb.pack(anchor=tk.W)
                        if n == 0:
                            rdb.select()
                        rdb.update()

                        c_frame.pack(anchor=tk.W, padx=(23, 0))

                    ttk.Separator(self.chooser_internal_frame,
                                  orient=tk.HORIZONTAL).pack(pady=4, fill="x", expand=True)

                def chooser_packer(self, n_values, frame, num, conditions):

                    if len(conditions) == 1:
                        condition, = conditions
                        options = [option.name for option in condition.__subclasses__()]
                    else:
                        values_1 = [option.name for option in conditions[0].__subclasses__()]
                        values_2 = [option.name for option in conditions[1].__subclasses__()]

                        options = [value for value in values_1 if value in values_2]

                    # options.sort()

                    choosers = []

                    for n in range(num):
                        choosers.append(ttk.Combobox(frame,
                                                     state="readonly",
                                                     width=16,
                                                     values=options))

                    n1, n2 = n_values

                    self.selectors[n1]["choosers"][n2] = (choosers, options)

                def chooser_checker(self):

                    for keys, values in self.selectors.items():
                        current_choice = values["current_choice"].get()

                        for keys_2, values_2 in values["choosers"].items():
                            widgets = values_2[0]
                            for widget in widgets:
                                parent_widget = widget._nametowidget(widget.winfo_parent())
                                widget.pack_forget()

                            if current_choice == keys_2:
                                for widget in widgets:
                                    widget.pack(pady=2)
                            else:
                                dummy = tk.Frame(parent_widget)
                                dummy.pack()
                                self.chooser_frame_dummies.append(dummy)

                    self.update_size()

                    self.get()

                def update(self, char, equipment_choices):
                    for child in self.chooser_internal_frame.winfo_children():
                        child.destroy()

                    end_text = []

                    self.selectors = {}

                    for n, choice in enumerate(equipment_choices):
                        if len(choice) > 1:
                            selection_variable = tk.IntVar()
                            self.selectors[n] = {"current_choice": selection_variable}
                            self.selector_packer(n, choice, selection_variable)
                        else:
                            end_text.append(choice[0][0].syntax(choice[0][1]))

                    self.end_label['text'] = helpers.list_syntax(end_text).capitalize()

                    self.chooser_checker()

                    # self.chooser_internal_frame.update()
                    # self.chooser_frame.update()
                    #
                    # self.chooser_internal_frame.config(relief=tk.RIDGE,
                    #                                    borderwidth=2)
                    # # self.chooser_internal_frame.pack_propagate(0)
                    # # self.chooser_internal_frame.config(width=self.chooser_frame.winfo_width())
                    #
                    # self.chooser_frame.config(width=400)

                    # print(self.chooser_internal_frame.winfo_reqwidth())
                    # print(self.chooser_frame.winfo_reqwidth())

                def get(self):

                    selected = []
                    chosen = []

                    for index, vals in self.selectors.items():
                        selected.append(vals["current_choice"].get())
                        for key, vals2 in vals["choosers"].items():
                            chosen.append([widget.get() for widget in vals2[0]])

                    values = {"selected": selected,
                              "chosen": chosen}

                    return values

                def set(self, values):
                    i = 0
                    j = 0
                    for index, vals in self.selectors.items():
                        vals["current_choice"].set(values["selected"][i])
                        i += 1
                        for key, vals2 in vals["choosers"].items():
                            for widget in vals2[0]:
                                widget.set(values["chosen"][j])
                                j += 1

                    self.chooser_checker()

            self.class_equipment_chooser = EquipmentChooser(self)

            Aspect(aspect_id="Class Equipment",
                   aspect_tab=Tabs.class_,
                   aspect_type=AspectTypes.equipment,
                   variable=self.class_equipment_chooser,
                   widget=self.right_frame, # ???
                   order=1,
                   active=True).add(self)

        def class_changed(*args):
            self.class_features_frame.grid_forget()

            self.class_instance = {c.class_name: c for c in classes.CharacterClass.__subclasses__()}[
                self.character_class.get()]

            self.class_desc['text'] = self.class_instance.desc
            self.class_rpgbot['text'] = self.class_instance.rpgbot
            self.class_hit_die.set(f"d{self.class_instance.hit_die}")

            if len(self.class_instance.primary_attr) > 1:
                self.class_attr_label['text'] = "Primary Attributes:"
            else:
                self.class_attr_label['text'] = "Primary Attribute:"

            self.class_primary_attr.set(helpers.list_syntax([attr.name for attr in self.class_instance.primary_attr]))

            profs = {"class_armour_profs": "armour_proficiencies",
                     "class_weapon_profs": "weapon_proficiencies",
                     "class_tool_profs": "tool_proficiencies"}

            for prof_string, prof_vals in profs.items():

                prof_string = getattr(self, prof_string)
                prof_vals = getattr(self.class_instance, prof_vals)

                if prof_vals:

                    names = []

                    for val in prof_vals:
                        names.append(val.uncountable())

                    vals = helpers.list_syntax(names)
                    vals = vals.lower().capitalize()
                else:
                    vals = None
                prof_string.set(vals)

            # Saves
            self.class_saving_throws.set(" and ".join([save.name for save in self.class_instance.saving_throws]))

            # Skills
            self.class_skills_chooser.deactivate()
            self.class_skills_chooser.values = [skill.name for skill in self.class_instance.valid_skills]
            self.class_skills_chooser.activate(self.class_instance.num_skills)

            # Equipment
            self.class_equipment_chooser.update(self, self.class_instance.equipment)

            self.class_features_frame.grid(row=2, padx=8)

            self.resize_tabs()

        ### Begin Code

        self.reset_tab_aspects(Tabs.class_)

        self.class_frame = tk.Frame(self.class_tab,
                                    relief=tk.SUNKEN,
                                    borderwidth=4,
                                    )

        self.class_label = tk.Label(self.class_frame,
                                    text="Class",
                                    font=default_font + " 12 bold").grid(row=0, columnspan=3, pady=8)

        class_choice_config()
        class_info_config()
        class_stats_config()
        class_skills_config()
        class_equipment_config()

        self.class_frame.pack(fill="both", expand=True)

        self.class_frame.grid_rowconfigure(0, weight=1)
        self.class_frame.grid_columnconfigure(0, weight=1)

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

    def __init__(self, char, window):
        self.master = window
        window.title("Character Creator")

        self.aspects = {}

        # character_creator = tk.Frame(window)
        # character_creator.pack()

        self.create_title()
        self.create_tab_manager()
        self.create_info_tab()
        self.create_race_tab()
        self.create_class_tab()

        # Move window to centre

        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()
        position_right = int(window.winfo_screenwidth() / 3 - windowWidth / 2)
        position_down = int(window.winfo_screenheight() / 4 - windowHeight / 2)
        window.geometry(f"+{position_right}+{position_down}")


if __name__ == "__main__":
    class Character:
        pass


    window = tk.Tk()
    char = Character
    CharacterCreator(char, window)
    style = ttk.Style(window)
    style.configure('TNotebook', tabposition='n')

    # style.map('TCombobox', fieldbackground=[('readonly', 'white')])
    # style.map('TCombobox', selectbackground=[('readonly', 'white')])
    # style.map('TCombobox', selectforeground=[('readonly', 'black')])
    # style.map('TCombobox', selectborderwidth=[('readonly', '0')])

    window.mainloop()
