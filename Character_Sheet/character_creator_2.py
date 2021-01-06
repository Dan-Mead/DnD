import pickle
import tkinter as tk
from functools import partial
from tkinter import filedialog
from tkinter import ttk

import Character_Sheet.reference.glossary as glossary
import Character_Sheet.reference.races as races

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


class AspectTypes:
    info = "info"
    skill = "skill"
    language = "language"
    asi = "asi"
    feat = "feat"
    race_feature_choice = "race feature choice"
    prof = "proficiency"


class Tabs:
    info = "info"
    race = "race"
    _class = "class"
    background = "background"


class ValueChooserGenerator:
    def __init__(self, character, master, num_choosers, variable_name, value_tab, value_type,
                 invalid_options=[], default_value="", values=[], label={}, grid={}, check_global=False, aspect_order = 1):
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
                                             values=[race for race in races.race_list],
                                             state="readonly",
                                             width=16,
                                             textvariable=self.character_race,
                                             justify="center")

            Aspect("Race", Tabs.race, AspectTypes.info, self.character_race, self.race_chooser, 0, True).add(self)

            race_choice_prompt = "Choose race: "
            self.race_chooser.set(race_choice_prompt)

            self.character_race.trace_add('write', race_changed)

            self.race_chooser.grid(row=1, columnspan=3, pady=2)

        def race_changed(*args):
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
                self.subrace_instance = {subrace.subrace_name: subrace for subrace in self.race_instance.__subclasses__()}[
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
                pack_race_asi(instance)
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

        def pack_race_asi(instance):

            for asi in self.asi_automatic_values:
                asi['text'] = ""

            self.asi_frame.grid(row=2, column=0)
            self.bottom_divider.grid(column=0, row=5, columnspan=3, sticky="EW", pady=(4, 0))

            try:
                asi_list = list(instance.ASI)
            except Exception as e:
                print(e)

            all_asi = asi_list  # + subrace specifics

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

            self.race_features_frame = tk.Frame(self.race_frame)

            self.race_features_title = tk.Label(self.race_features_frame,
                                                text="Racial Features:",
                                                font=default_font + " 10 bold",
                                                anchor="n")

            self.race_features_title_frame = tk.Frame(self.race_features_frame)
            self.race_features_chooser_frame = tk.Frame(self.race_features_title_frame)
            self.race_features_general_frame = tk.Frame(self.race_features_frame)

            self.subrace_features_title_frame = tk.Frame(self.race_features_frame)
            self.subrace_features_chooser_frame = tk.Frame(self.subrace_features_title_frame)
            self.subrace_features_general_frame = tk.Frame(self.race_features_frame)

            self.race_features_label = tk.Label(self.race_features_title_frame,
                                                text="Race Features:",
                                                font=default_font + " 8 bold",
                                                anchor="n")
            self.subrace_features_label = tk.Label(self.subrace_features_title_frame,
                                                   text="Subrace Features:",
                                                   font=default_font + " 8 bold",
                                                   anchor="n")

            self.race_features_label.pack()
            self.subrace_features_label.pack()
            self.race_features_chooser_frame.pack()
            self.subrace_features_chooser_frame.pack()

            self.racial_features = dict(race=[], subrace=[])
            self.racial_widgets_activatable = []
            self.racial_feature_choosers = dict(race=[], subrace=[])

        def feature_changed(*args):

            pack_features_list()

        def pack_other_features(instance, is_subrace):

            if is_subrace:
                key = 'subrace'
                chooser_frame = self.subrace_features_chooser_frame
                aspect_label = self.subrace_instance.subrace_name

            else:
                key = 'race'
                chooser_frame = self.race_features_chooser_frame
                aspect_label = self.race_instance.race_name

            self.racial_features['subrace'] = []
            if not is_subrace:
                self.racial_features['race'] = []

            if instance.features:
                self.divider_2.grid(row=3, column=1, sticky="NS", rowspan=8)
                self.race_features_title.grid(row=0)
                self.race_features_frame.grid(row=3, column=2, sticky="N", padx=4)

                if not is_subrace:
                    self.race_features_title_frame.grid(row=1, sticky="N")
                    self.race_features_general_frame.grid(row=2)

                    self.subrace_features_title_frame.grid_forget()
                    self.subrace_features_general_frame.grid_forget()

                else:
                    self.subrace_features_title_frame.grid(row=3, sticky="N")
                    self.subrace_features_general_frame.grid(row=4)

                # If choices to be made

                if races.FeatureType.choice in instance.features.types:

                    for child in chooser_frame.winfo_children():
                        child.destroy()

                    if not is_subrace:
                        for chooser in self.racial_feature_choosers['race']:
                            chooser[0].deactivate()
                        self.racial_feature_choosers['race'] = []

                    for chooser in self.racial_feature_choosers['subrace']:
                        chooser[0].deactivate()
                    self.racial_feature_choosers['subrace'] = []
                    for feature_name, feature_vals in instance.features.all.items():
                        if feature_vals[0] == races.FeatureType.choice:
                            chooser_label = tk.Label(chooser_frame,
                                                     text=feature_name,
                                                     font=default_font + " 8")
                            chooser_label.pack()

                            chooser = ValueChooserGenerator(character=self,
                                                            master=chooser_frame,
                                                            num_choosers=1,
                                                            variable_name=f"{aspect_label} Features Choice",
                                                            value_tab=Tabs.race,
                                                            value_type=AspectTypes.race_feature_choice,
                                                            default_value=f"Choose {key} feature:",
                                                            values=feature_vals[1],
                                                            check_global=True
                                                            )
                            chooser.widgets[0]["width"] = 20

                            chooser.activate()

                            chooser_feature_frame = tk.Frame(chooser_frame)

                            choice_variable = chooser.variables[0]

                            self.racial_feature_choosers[key].append(
                                (chooser, choice_variable, feature_vals[1], chooser_feature_frame))

                            choice_variable.trace_add("write", feature_changed)

                else:
                    for chooser in self.racial_feature_choosers['subrace']:
                        chooser[0].deactivate()
                    self.racial_feature_choosers['subrace'] = []

                    for child in self.subrace_features_chooser_frame.winfo_children():
                        child.destroy()

                    tk.Frame(self.subrace_features_chooser_frame).pack()

                    if not is_subrace:

                        for chooser in self.racial_feature_choosers['race']:
                            chooser[0].deactivate()
                        self.racial_feature_choosers['race'] = []

                        for child in self.race_features_chooser_frame.winfo_children():
                            child.destroy()

                        tk.Frame(self.race_features_chooser_frame).pack()

                self.racial_features[key] = instance.features.all

                pack_features_list()

            elif not is_subrace or not self.race_instance.features:

                self.divider_2.grid_forget()
                self.race_features_title.grid_forget
                self.race_features_frame.grid_forget()

                self.race_features_title_frame.grid_forget()
                self.race_features_general_frame.grid_forget()
                self.subrace_features_title_frame.grid_forget()
                self.subrace_features_general_frame.grid_forget()
            elif is_subrace:

                self.subrace_features_title_frame.grid_forget()
                self.subrace_features_general_frame.grid_forget()

        def pack_features_list():

            class FeatureWidgets:
                def __init__(self, char):
                    self.char = char

                def chooser(self, feature_name, feature_frame, feature_values):
                    pass

                def other(self, feature_name, feature_frame, feature_values):
                    widget = tk.Label(feature_frame,
                                      text=f'{feature_values.desc}\n',
                                      wraplength=400,
                                      justify=tk.LEFT,
                                      anchor="w",
                                      font=default_font + " 8"
                                      )
                    widget.pack(side=tk.LEFT)

                def skill(self, feature_name, feature_frame, feature_values):
                    for n, values in enumerate(feature_values):
                        widget = ValueChooserGenerator(character=self.char,
                                                       master=feature_frame,
                                                       num_choosers=1,
                                                       variable_name=f"{feature_name} Skill {n}",
                                                       value_tab=Tabs.race,
                                                       value_type=AspectTypes.skill,
                                                       default_value=f"Choose skill:",
                                                       values=values,
                                                       aspect_order=2,
                                                       check_global=True
                                                       )
                        widget.activate()
                        self.char.racial_widgets_activatable.append(widget)

                def feat(self, feature_name, feature_frame, feature_values):
                    for n, values in enumerate(feature_values):
                        widget = ValueChooserGenerator(character=self.char,
                                                       master=feature_frame,
                                                       num_choosers=1,
                                                       variable_name=f"{feature_name} Feat {n}",
                                                       value_tab=Tabs.race,
                                                       value_type=AspectTypes.feat,
                                                       default_value=f"Choose feat:",
                                                       values=values,
                                                       aspect_order=2,
                                                       check_global=True)
                        widget.activate()  # Add prereq here
                        self.char.racial_widgets_activatable.append(widget)

                def prof(self, feature_name, feature_frame, feature_values):
                    prof_type = feature_values[0]
                    feature_vals = feature_values[1]

                    widget = ValueChooserGenerator(character=self.char,
                                                   master=feature_frame,
                                                   num_choosers=1,
                                                   variable_name=f"{feature_name} {prof_type}",
                                                   value_tab=Tabs.race,
                                                   value_type=AspectTypes.prof,
                                                   default_value=f"Choose {prof_type} proficiency:",
                                                   values=feature_vals,
                                                   aspect_order=2,
                                                   check_global=True)

                    widget.widgets[0]["width"] = len(widget.default_value) - 4

                    widget.activate()
                    self.char.racial_widgets_activatable.append(widget)

            for widget in self.racial_widgets_activatable:
                widget.deactivate()

            packer = FeatureWidgets(self)

            feature_switcher = {
                races.FeatureType.choice: packer.chooser,
                races.FeatureType.other: packer.other,
                races.FeatureType.skills: packer.skill,
                races.FeatureType.feats: packer.feat,
                races.FeatureType.proficiencies: packer.prof
            }

            class FeatureSet:
                def __init__(self, name, master_frame, features):
                    self.name = name
                    self.master = master_frame
                    self.features = features

            race_set = FeatureSet('race', self.race_features_general_frame, self.racial_features['race'])
            subrace_set = FeatureSet('subrace', self.subrace_features_general_frame, self.racial_features['subrace'])

            for set in [race_set, subrace_set]:

                for child in set.master.winfo_children():
                    child.destroy()

                if set.features:
                    for feature_name, feature_val in set.features.items():
                        feature_frame = tk.Frame(set.master)
                        feature_label = tk.Label(feature_frame,
                                                 text=feature_name,
                                                 font=default_font + " 8")

                        if not isinstance(feature_val, list):
                            feature_type, feature_values = feature_val
                            if feature_type != races.FeatureType.choice:
                                feature_label.pack()
                            try:
                                feature_switcher[feature_type](feature_name, feature_frame, feature_values)
                            except Exception as e:
                                print(f'Error on {e} key for {feature_name}')

                        else:
                            feature_label.pack()
                            for pair in feature_val:
                                feature_type, feature_values = pair
                                try:
                                    feature_switcher[feature_type](feature_name, feature_frame, feature_values)
                                except Exception as e:
                                    print(f'Error on {e} key for {feature_name}')

                        feature_frame.pack(fill="x", expand=True)

            for info_set, choosers in self.racial_feature_choosers.items():
                if choosers:

                    for choice_info in choosers:
                        chooser, choice_variable, feature_options, chooser_frame = choice_info
                        default = chooser.default_value
                        choice_name = choice_variable.get()

                        for child in chooser_frame.winfo_children():
                            child.destroy()

                        if choice_name != default:

                            choice_options = feature_options[choice_name]
                            if isinstance(choice_options, list):
                                for options in choice_options:
                                    choice_type = options[0]
                                    choice_values = options[1]
                                    feature_switcher[choice_type](feature_name, chooser_frame, choice_values)
                            else:
                                choice_type = choice_options[0]
                                choice_values = choice_options[1]
                                feature_switcher[choice_type](feature_name, chooser_frame, choice_values)

                            chooser_frame.pack()

            self.resize_tabs()

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

        self.race_frame.pack(fill="both", expand=True)

        self.race_frame.grid_rowconfigure(0, weight=1)
        self.race_frame.grid_columnconfigure(0, weight=1)

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
        # Info().pack()
        # Class().pack()
        # Race().pack()
        # Background_().pack()

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
