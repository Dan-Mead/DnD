import pickle
import textwrap
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from Character_Sheet.reference.backgrounds import *
from Character_Sheet.reference.feats import feat_list, unpack_desc
from Character_Sheet.reference.glossary import common_languages, \
    exotic_languages, attrs
from Character_Sheet.reference.races import race_list
from Character_Sheet.reference.subclasses import *

# from Character_Sheet.reference.equipment import Martial, Simple, Ranged, Melee

global current_race_instance, current_subrace_instance


# System Functions

def export(character):
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


def update_character_info():
    character_data = {}
    for name, item in character.items():

        if isinstance(item, (list, tuple)):
            print("Alternative methods required")
        elif isinstance(item, dict):
            character_data[name] = {}
            for key, value in item.items():
                if not isinstance(value[0], (list, tuple)):
                    character_data[name][key] = [val.get() for val in value]
                else:
                    character_data[name][key] = [[v.get() for v in val] for val
                                                 in value]
        else:
            character_data[name] = item.get()

    return character_data


def save():
    data = update_character_info()
    export(data)


def load():
    filename = tk.filedialog.askopenfilename(initialdir="saves/",
                                             title="Select save file",
                                             filetypes=(
                                                 ("Pickled Files", "*.pkl"),
                                                 ("all files", "*.*")))

    character_data = import_info(filename)

    second_stage_imports = []

    for key, value in character_data.items():
        try:
            input = character_data[key]
            destination = character[key]
            if isinstance(destination, tk.ttk.Combobox) or isinstance(
                    destination, tk.StringVar):
                destination.set(input)
            elif isinstance(destination, dict):
                second_stage_imports.append((key, value))
            else:
                destination.delete(0, tk.END)
                destination.insert(0, input)
        except Exception as print_error:
            print(key)
            print(character[key])
            print(value)
            print(print_error)

    for aspect in second_stage_imports:
        key, value = aspect
        for subkey, subvalue in value.items():
            update_character_info()
            if not isinstance(subvalue[0], (list, tuple)):
                for n, variable in enumerate(character[key][subkey]):
                    variable.set(subvalue[n])
            else:
                for i, sublist in enumerate(character[key][subkey]):
                    for j, variable in enumerate(sublist):
                        variable.set(subvalue[i][j])

    resize_tabs()


def save_and_close():
    save()
    window.destroy()


def close():
    window.destroy()


def exit():
    def exit_save_and_close():
        save_and_close()
        exit_window.destroy()

    def exit_close():
        close()
        exit_window.destroy()

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


# Helper Functions

def get_chosen_skills(character):
    return [character[choice].get() for choice in character.keys() if
            "Skill" in choice]


def text_join(text, capitalise, sentence_end):
    if len(text) > 2:
        text = ", ".join(text[:-1]) + f", and {text[-1]}"
    else:
        text = " and ".join(text)

    text += sentence_end

    if capitalise:
        text = text[0].upper() + text[1:]

    return text


# Creation of Frames

def Title():
    title = tk.Label(character_creator,
                     text='Character Creator',
                     bd=8,
                     font=default_font + " 14 bold")

    title.pack(side=tk.TOP)

    main_menu = tk.Menu(character_creator)

    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Save", command=save)
    file_menu.add_command(label="Load", command=load)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit)
    main_menu.add_cascade(label="File", menu=file_menu)

    window.config(menu=main_menu)


def Info():
    info_frame = tk.Frame(info_tab,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )

    ### Character Name

    name_frame = tk.Frame(info_frame)

    name_label = tk.Label(name_frame,
                          text='Character name',
                          font=default_font + " 12 bold")
    name_entry = tk.Entry(name_frame,
                          width=24,
                          justify="center")

    name_label.pack()
    name_entry.pack()

    name_frame.pack(padx=8, pady=(8, 16))

    ### Character info

    data_frame = tk.Frame(info_frame)

    #### Age

    age_frame = tk.Frame(data_frame)

    age_label = tk.Label(age_frame,
                         text="Age",
                         font=default_font + " 10 bold")
    age_entry = tk.Entry(age_frame,
                         width=8,
                         justify="center")

    age_label.grid(row=0)
    age_entry.grid(row=1)

    #### Gender

    gender_frame = tk.Frame(data_frame)

    gender_label = tk.Label(gender_frame,
                            text="Gender",
                            font=default_font + " 10 bold")
    gender_entry = tk.Entry(gender_frame,
                            width=8,
                            justify="center")

    gender_label.grid(row=0)
    gender_entry.grid(row=1)

    #### Physical Attributes

    appearance_aspects = ["Skin Colour",
                          "Hair Colour",
                          "Eye Colour"]
    size_aspects = ["Height",
                    "Weight",
                    "Build"]

    appearance_frame = tk.Frame(data_frame)
    size_frame = tk.Frame(data_frame)

    physicals = {}

    for j in range(len(appearance_aspects)):

        frames = appearance_frame, size_frame
        aspects = appearance_aspects, size_aspects

        for k, frame in enumerate(frames):
            label = tk.Label(frame,
                             text=aspects[k][j],
                             font=default_font + " 10 bold")
            entry = tk.Entry(frame,
                             width=10,
                             justify="center")

            physicals[label.cget("text")] = entry

            label.grid(row=1, column=j, pady=(2, 1), padx=4)
            entry.grid(row=2, column=j, padx=8)

    ### Add all data to frame

    age_frame.grid(row=0, column=0, padx=(0, 4), sticky="E")
    gender_frame.grid(row=0, column=1, padx=(4, 0), sticky="W")
    appearance_frame.grid(row=2, column=0, columnspan=2, padx=(0, 8))
    size_frame.grid(row=4, column=0, columnspan=2, padx=(8, 0))

    data_frame.pack()

    ### Faith

    faith_frame = tk.Frame(info_frame)

    faith_label = tk.Label(faith_frame,
                           text='Faith',
                           font=default_font + " 10 bold")
    faith_entry = tk.Entry(faith_frame,
                           width=16,
                           justify="center")

    faith_label.pack()
    faith_entry.pack()

    faith_frame.pack(pady=2)

    ### Alignment

    alignment_frame = tk.Frame(info_frame)

    alignment_label = tk.Label(faith_frame,
                               text='Alignment',
                               font=default_font + " 10 bold")

    alignment_entry_frame = tk.Frame(alignment_frame)

    ethics = ttk.Combobox(alignment_entry_frame,
                          values=["Lawful", "Neutral", "Chaotic"],
                          state="readonly",
                          width=8)
    morality = ttk.Combobox(alignment_entry_frame,
                            values=["Good", "Neutral", "Evil"],
                            state="readonly",
                            width=8)

    ethics.grid(row=0, column=1, padx=(0, 2))
    morality.grid(row=0, column=2, padx=(2, 0))

    alignment_label.pack()
    alignment_entry_frame.pack()

    alignment_frame.pack(pady=2)

    ### Character Info for Export

    character_info = {"Name": name_entry,
                      "Age": age_entry,
                      "Gender": gender_entry,
                      "Faith": faith_entry,
                      "Ethics": ethics,
                      "Morality": morality
                      }

    character_info.update(physicals)

    character.update(character_info)

    return info_frame


def Race():
    def update_race_info():

        for key, value in race_data.items():
            if key != "Race" and key != "Subrace":
                value.set("")

        size = current_race_instance.size
        speed = current_race_instance.speed
        race_size_text.set(size)
        race_speed_text.set(f'{speed} ft.')

        if current_race_instance.__subclasses__():
            subrace_choice.pack()
            if current_subrace.get() != '':
                subrace_choice.set(current_subrace.get())
            else:
                subrace_choice.set(subrace_choice_prompt)
            subclass = True

        else:
            current_subrace.set(None)
            subrace_choice.pack_forget()
            subclass = False
            subrace_choice.set("")

        race_info.pack_forget()
        race_info.pack()
        race_languages_choice.grid_forget()
        race_base_info.update()
        languages()

        if not subclass:
            ASI()
            other_features()

    def languages():

        language_list = [language for language in
                         current_race_instance.languages]

        choices_num = language_list.count("choice")

        if choices_num > 0:
            language_list.remove("choice")
            race_languages_choice.grid(row=3, column=2, stick="W", padx=(2, 0))

            divider.grid(rowspan=race_base_info.grid_size()[1])

            known_languages = language_list
            language_choices = ["None"] + common_languages + exotic_languages
            for lang in known_languages:
                language_choices.remove(lang)
            race_languages_choice["values"] = language_choices

        language_list = "\n".join(language_list)

        race_language_text.set(language_list)

    def ASI():

        bottom_divider.grid(column=0, row=5, columnspan=3, sticky="EW",
                            pady=(4, 0))

        if current_subrace_instance is None:
            ASI = current_race_instance.ASI
        else:
            ASI = current_subrace_instance.ASI

        num_choices = 0
        choice_options = []

        for i in ASI:
            if i[0] == "choice":
                num_choices += 1
                choice_options.append(i[1])

        ASI_automatic = dict(ASI)

        if num_choices > 0:
            del ASI_automatic["choice"]

        if ASI_automatic:
            asi_attributes_frame.grid(row=1)
            for asi_value in asi_automatic_values:
                asi_value.configure(text="")

            for attribute, attr_value in ASI_automatic.items():
                attr_index = attrs.index(attribute.__name__)

                text_value = f'{attr_value:+d}'

                asi_automatic_values[attr_index].configure(text=text_value)
        else:
            asi_attributes_frame.grid_forget()

        asi_choice_frame.grid_forget()

        if num_choices > 0:
            asi_choice_label["text"] = "Choose ability score to increase by +1:"
            asi_choice_frame.grid(row=2)
            asi_choice_2.grid_forget()
            if choice_options[0] == "any":
                asi_options = attrs.copy()
            else:
                asi_options = attrs.copy()
                asi_options.remove(choice_options[0])

            asi_choice_1_val = tk.StringVar()
            asi_choice_1["textvariable"] = asi_choice_1_val
            asi_choice_1["values"] = asi_options
        if num_choices == 2:
            asi_choice_label[
                "text"] = "Choose ability scores to increase by +1:"
            asi_choice_2.grid(row=2)
            asi_choice_2_val = tk.StringVar()
            asi_choice_2["textvariable"] = asi_choice_2_val

            def check_asi_1_choices():
                second_choice = asi_choice_2.get()
                if not second_choice:
                    pass
                else:
                    first_options = asi_options.copy()
                    first_options.remove(second_choice)
                    asi_choice_1["values"] = first_options

            def check_asi_2_choices():
                first_choice = asi_choice_1.get()
                second_options = asi_options.copy()
                second_options.remove(first_choice)
                asi_choice_2["values"] = second_options

            asi_choice_1["postcommand"] = check_asi_1_choices
            asi_choice_2["postcommand"] = check_asi_2_choices

        asi_frame.grid(row=2, column=0)

    def other_features():

        race_features_frame.grid_forget()
        divider_2.grid_forget()

        for widget in race_features_internal_frame.winfo_children():
            widget.pack_forget()

        if current_race_instance.features:
            race_features = current_race_instance.features.copy()
            try:
                race_features += current_race_instance.features_chosen
            except:
                pass
        else:
            race_features = None

        if current_subrace_instance and current_subrace_instance.features:
            subrace_features = current_subrace_instance.features.copy()
            try:
                subrace_features += current_subrace_instance.features_chosen
            except:
                pass
        else:
            subrace_features = None

        if not (race_features or subrace_features):
            return
        else:
            race_info.update()
            # TODO: Make row here more intelligent
            race_features_frame.grid(row=0, column=2, rowspan=8, sticky="N")
            divider_2.grid(column=1, row=0, sticky="NS", rowspan=8)

        if race_features:
            features_checker(current_race_instance, race_features)

        if subrace_features:
            features_checker(current_subrace_instance, subrace_features)

    def feature_switch(entity, feature):
        if feature == "skills":
            skills(entity.skills)
        elif feature == "feat":
            feat(entity.feats)
        elif feature == "other":
            others(entity.other_features)
        elif feature == "choice":
            feature_choice(entity)

    def features_checker(entity, features):

        for feature in features:
            feature_switch(entity, feature)

    def feature_choice(entity):

        options = list(entity.choice_features.keys())

        if entity.__subclasses__():
            if race_feature_chosen.get() not in options:
                race_feature_chosen.set("")
            race_feature_chooser["values"] = options
            subrace_feature_chooser_label.pack_forget()
            subrace_feature_chooser.pack_forget()

        else:
            if subrace_feature_chosen.get() not in options:
                subrace_feature_chosen.set("")
            subrace_feature_chooser["values"] = options
            race_feature_chooser_label.pack_forget()
            race_feature_chooser.pack_forget()

        race_feature_chooser_frame.pack()

    def skills(valid_skills):

        def choose_race_skill():

            chosen_skills = get_chosen_skills(character)

            for n, valid_skill in enumerate(valid_skills):

                invalid_skills = chosen_skills.copy()

                invalid_skills.remove(race_skills_choices[n].get())

                if isinstance(valid_skill, str) and valid_skill == "any":
                    valid_choices = [skill for skill in skills_list if
                                     skill not in invalid_skills]

                race_skill_choosers[n]["value"] = valid_choices

        skill_chooser_1["postcommand"] = choose_race_skill
        skill_chooser_2["postcommand"] = choose_race_skill

        for n, skill_chooser in enumerate(race_skill_choosers):
            try:
                if valid_skills[n] != "any" and skill_chooser.get() not in \
                        valid_skills[n]:
                    race_skills_choices[n].set(skill_chooser.get())
                skill_chooser.pack()
            except:
                skill_chooser.set("")
                skill_chooser.pack_forget()

        skill_chooser_frame.pack()

    def feat(valid_feats):

        feat_chooser.set("")

        if valid_feats == "any":
            valid_feats_name_list = tuple([name for name in feat_list.keys()])
        else:  # TODO: This is incomplete, also need to check for prereq
            valid_feats_name_list = tuple()

        feat_chooser["values"] = valid_feats_name_list
        feat_chooser_frame.pack()

    def others(other_features):
        text = ""
        for name, feature in other_features.items():
            text += f'{name}:'
            text += f'\n{feature.desc}\n\n'
        text = text[:-1]
        general_features_text.set(text)
        general_features_frame.pack()

    # Chosing Race and Subrace
    race_frame = tk.Frame(race_tab,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )
    race_label = tk.Label(race_frame,
                          text="Race",
                          font=default_font + " 12 bold")
    race_label.pack(pady=(8, 8))
    current_race = tk.StringVar()
    race_choice = ttk.Combobox(race_frame,
                               values=[race for race in race_list],
                               state="readonly",
                               width=16,
                               textvariable=current_race)

    race_choice_prompt = "Choose race: "
    race_choice.set(race_choice_prompt)

    subrace_choice_prompt = "Choose subrace: "
    current_subrace = tk.StringVar()

    def get_subclasses():
        subrace_choice["values"] = [subrace.subrace_name for subrace in
                                    current_race_instance.__subclasses__()]

    subrace_choice = ttk.Combobox(race_frame,
                                  postcommand=get_subclasses,
                                  values=[],
                                  state="readonly",
                                  width=16,
                                  textvariable=current_subrace)

    # Race Info Stuff
    race_info = tk.Frame(race_frame)

    race_info_label = tk.Label(race_info,
                               text="Racial Stats:",
                               font=default_font + " 10 bold")

    race_size_text = tk.StringVar()
    race_speed_text = tk.StringVar()
    race_language_text = tk.StringVar()

    race_size_text.set("Medium")
    race_speed_text.set(f'{30} ft.')
    race_language_text.set("Common")

    race_base_info = tk.Frame(race_info)

    race_size_label = tk.Label(race_base_info,
                               text="Size",
                               font=default_font + " 10 bold")
    race_speed_label = tk.Label(race_base_info,
                                text="Speed",
                                font=default_font + " 10 bold")
    divider = ttk.Separator(race_base_info,
                            orient=tk.VERTICAL)

    race_size_value = tk.Label(race_base_info,
                               textvariable=race_size_text,
                               font=default_font + " 10")

    race_speed_value = tk.Label(race_base_info,
                                textvariable=race_speed_text,
                                font=default_font + " 10")

    race_languages_label = tk.Label(race_base_info,
                                    text="Languages",
                                    font=default_font + " 10 bold")

    race_languages_value = tk.Label(race_base_info,
                                    textvariable=race_language_text,
                                    font=default_font + " 10",
                                    justify=tk.LEFT)

    race_languages_choice = ttk.Combobox(race_base_info,
                                         values=[],
                                         state="readonly",
                                         width=16)

    race_languages_choice.set("Choose language: ")

    race_size_label.grid(row=0, column=0, sticky="E")
    race_size_value.grid(row=0, column=2, sticky="W")
    race_speed_label.grid(row=1, column=0, sticky="E")
    race_speed_value.grid(row=1, column=2, sticky="W")
    race_languages_label.grid(row=2, column=0, sticky="NE")
    race_languages_value.grid(row=2, column=2, sticky="NW")

    divider.grid(column=1, row=0, rowspan=race_base_info.grid_size()[1],
                 sticky="NS")

    bottom_divider = ttk.Separator(race_base_info)
    bottom_divider.grid(column=0, row=5, columnspan=3, sticky="EW", pady=(4, 0))

    race_info_label.grid(row=0)
    race_base_info.grid(row=1, column=0, sticky="N")

    # Tracing Race/Subrace values
    def changed_race(*args):
        global current_race_instance
        if current_race.get() != race_choice_prompt:  # essential to call the variable once, no idea why
            current_race_instance = race_list[current_race.get()]
            asi_frame.grid_forget()
            bottom_divider.grid_forget()
            current_subrace.set(subrace_choice_prompt)
            update_race_info()
        else:
            current_race_instance = None

        resize_tabs()

    current_race.trace('w', changed_race)

    def changed_subrace(*args):
        global current_subrace_instance

        if current_race.get() != 'Choose race: ':

            if race_list[
                current_race.get()].__subclasses__() and current_subrace.get() != subrace_choice_prompt:
                current_subrace_instance = \
                    {subrace.subrace_name: subrace for subrace in
                     current_race_instance.__subclasses__()}[
                        current_subrace.get()]
                asi_frame.grid_forget()
                bottom_divider.grid_forget()
                ASI()
                other_features()

            elif current_subrace.get() == subrace_choice_prompt:
                race_features_frame.grid_forget()
                current_subrace_instance = None

            resize_tabs()

    current_subrace.trace('w', changed_subrace)

    # ASI Stuff
    asi_frame = tk.Frame(race_info)

    asi_label = tk.Label(asi_frame,
                         text="Ability score increases",
                         font=default_font + " 8 bold")

    asi_label.grid(row=0, sticky="N")

    asi_attributes_frame = tk.Frame(asi_frame)

    asi_automatic_values = [None] * 6
    for n, attribute in enumerate(attrs):
        label = tk.Label(asi_attributes_frame,
                         text=attribute,
                         font=default_font + " 10 bold")
        label.grid(row=n, column=0, sticky="E")

        value = tk.Label(asi_attributes_frame,
                         font=default_font + " 10")

        value.grid(row=n, column=2, sticky="W")
        asi_automatic_values[n] = value

    ttk.Separator(asi_attributes_frame,
                  orient=tk.VERTICAL).grid(column=1, row=0, sticky="NS",
                                           rowspan=
                                           asi_attributes_frame.grid_size()[1])

    asi_choice_frame = tk.Frame(asi_frame)

    asi_choice_label = tk.Label(asi_choice_frame,
                                text="Choose ability score to increase by +1:")

    asi_choice_1 = ttk.Combobox(asi_choice_frame,
                                state="readonly",
                                width=12)

    asi_choice_2 = ttk.Combobox(asi_choice_frame,
                                state="readonly",
                                width=12)

    asi_choice_label.grid(row=0)
    asi_choice_1.grid(row=1)
    asi_choice_2.grid(row=2)

    asi_attributes_frame.grid(row=1)
    asi_choice_frame.grid(row=2)

    race_choice.pack()

    # Race Features
    race_features_frame = tk.Frame(race_info)

    race_features_label = tk.Label(race_features_frame,
                                   text="Racial Features:",
                                   font=default_font + " 10 bold",
                                   anchor="n")
    race_features_label.grid(row=0, sticky="N")

    # race_features_frame.grid(row=0, column=2, sticky="N")

    divider_2 = ttk.Separator(race_info,
                              orient=tk.VERTICAL)

    # divider_2.grid(column=1, row=0, sticky="NS", rowspan=2)

    race_features_internal_frame = tk.Frame(race_features_frame)
    race_features_internal_frame.grid(row=1)

    skill_chooser_frame = tk.Frame(race_features_internal_frame)

    skill_chooser_label = tk.Label(skill_chooser_frame,
                                   text="Choose skill proficiency:",
                                   font=default_font + " 8")

    race_skill_choice_1 = tk.StringVar()
    race_skill_choice_2 = tk.StringVar()

    skill_chooser_1 = ttk.Combobox(skill_chooser_frame,
                                   state="readonly",
                                   textvariable=race_skill_choice_1)
    skill_chooser_label.pack(pady=(4, 0))
    skill_chooser_1.pack()

    skill_chooser_2 = ttk.Combobox(skill_chooser_frame,
                                   state="readonly",
                                   textvariable=race_skill_choice_2)
    skill_chooser_2.pack()

    race_skill_choosers = [skill_chooser_1, skill_chooser_2]
    race_skills_choices = [race_skill_choice_1, race_skill_choice_2]

    feat_chooser_frame = tk.Frame(race_features_internal_frame)

    feat_chooser_label = tk.Label(feat_chooser_frame,
                                  text="Choose feat:",
                                  font=default_font + " 8")
    feat_chosen = tk.StringVar()
    feat_chooser = ttk.Combobox(feat_chooser_frame,
                                textvariable=feat_chosen,
                                state="readonly")

    def changed_feat(*args):

        if feat_chosen.get():
            description = feat_list[feat_chosen.get()].desc
            description_formatted = unpack_desc(description)
            feat_description.set(description_formatted)

        resize_tabs()

    feat_chosen.trace('w', changed_feat)
    feat_description = tk.StringVar()

    feat_description_label = tk.Label(feat_chooser_frame,
                                      textvariable=feat_description,
                                      wraplength=400,
                                      justify=tk.LEFT,
                                      font=default_font + " 8")

    feat_chooser_label.pack()
    feat_chooser.pack()
    feat_description_label.pack()

    general_features_frame = tk.Frame(race_features_internal_frame)

    general_features_text = tk.StringVar()

    general_feature_label = tk.Label(general_features_frame,
                                     textvariable=general_features_text,
                                     wraplength=400,
                                     justify=tk.LEFT,
                                     anchor="w",
                                     font=default_font + " 8"
                                     )

    general_feature_label.pack(side=tk.LEFT)

    race_feature_chooser_frame = tk.Frame(race_features_internal_frame)
    race_feature_chooser_label = tk.Label(race_feature_chooser_frame,
                                          text="Choose racial feature:",
                                          font=default_font + " 8")

    subrace_feature_chooser_label = tk.Label(race_feature_chooser_frame,
                                             text="Choose subrace feature:",
                                             font=default_font + " 8")

    race_feature_chosen = tk.StringVar()
    subrace_feature_chosen = tk.StringVar()
    race_feature_chooser = ttk.Combobox(race_feature_chooser_frame,
                                        state="readonly",
                                        textvariable=race_feature_chosen)
    subrace_feature_chooser = ttk.Combobox(race_feature_chooser_frame,
                                           state="readonly",
                                           textvariable=subrace_feature_chosen)

    def race_feature_changed(*args):

        if race_feature_chosen.get():

            feature_value = current_race_instance.choice_features[
                race_feature_chosen.get()]

            current_race_instance.features_chosen = []

            if isinstance(feature_value, str):
                current_race_instance.features_chosen.append(feature_value)
                other_features()

            else:
                other_features()
                text = general_features_text.get()
                text += f'\n{race_feature_chosen.get()}:'
                text += f'\n{feature_value.desc}\n'
                general_features_text.set(text)
                general_features_frame.pack()

        resize_tabs()

    def subrace_feature_changed(*args):
        if subrace_feature_chosen.get():

            feature_value = current_subrace_instance.choice_features[
                subrace_feature_chosen.get()]

            current_subrace_instance.features_chosen = []

            if isinstance(feature_value, str):
                current_subrace_instance.features_chosen.append(feature_value)
                other_features()

            else:
                other_features()
                text = general_features_text.get()
                text += f'\n{subrace_feature_chosen.get()}:'
                text += f'\n{feature_value.desc}\n'
                general_features_text.set(text)
                general_features_frame.pack()

        resize_tabs()

    race_feature_chosen.trace("w", race_feature_changed)
    subrace_feature_chosen.trace("w", subrace_feature_changed)

    race_feature_chooser_label.pack(pady=(4, 0))
    race_feature_chooser.pack()
    subrace_feature_chooser_label.pack()
    subrace_feature_chooser.pack()

    race_info.update()

    race_data = {"Race": race_choice,
                 "Subrace": subrace_choice,
                 "Languages": race_languages_choice,
                 "ASI Choice 1": asi_choice_1,
                 "ASI Choice 2": asi_choice_2,
                 "Race Skill 1": skill_chooser_1,
                 "Race Skill 2": skill_chooser_2,
                 "Race Feat": feat_chooser,
                 "Race Feature": race_feature_chooser,
                 "Subrace Feature": subrace_feature_chooser
                 }

    character.update(race_data)

    return race_frame


def Class():
    def class_choice_changed(*args):
        global current_class_instance

        if current_class_choice.get() != "":
            current_class_instance = class_list[current_class_choice.get()]()
            class_ = current_class_instance
            class_.base_features()
            class_top_label["text"] = f"{class_.name} features:"
            text = ""

            text += f"Primary Attribute{'s' if len(current_class_instance.primary_attr) > 1 else ''}:\n"
            text += " and ".join([attr.name for attr in
                                  current_class_instance.primary_attr]) + "\n"

            text += f"\nSaving Throw Proficiencies:\n" \
                    f"{', '.join([class_.name if class_ else 'None' for class_ in class_.saving_throws])}\n"

            text += f"\nArmour Proficiencies:\n" \
                    f"{', '.join([class_.__name__ if class_ else 'None' for class_ in class_.armour_proficiencies])}\n"

            text += f"\nWeapon Proficiencies:\n" \
                    f"{', '.join([class_.name if class_ else 'None' for class_ in class_.weapon_proficiencies])}\n"

            text += f"\nTool Proficiencies:\n" \
                    f"{', '.join([class_.name if class_ else 'None' for class_ in class_.tool_proficiencies])}\n"

            text += f"\nHit Dice: {class_.hit_die}\n"
            text += f"Level up HP: {class_.lvl_up_hp}\n"

            class_basic_info_text["text"] = text

            class_left_frame.grid(column=0, row=0, sticky="n", padx=4)
            class_central_frame.grid(column=2, row=0, sticky="n", padx=4)
            class_right_frame.grid(column=4, row=0, sticky="n", padx=4)

            class_divider_1.grid(column=1, row=0, rowspan=10, sticky="NS")
            class_divider_2.grid(column=3, row=0, rowspan=10, sticky="NS")

            skill_choosers(current_class_instance)
            equipment_selection(current_class_instance)

            class_description.set(f'{class_.desc}\n\n\n{class_.rpgbot}')

            subclass_list = "\n".join(
                sorted([subclass.name for subclass in
                        current_class_instance.__class__.__subclasses__()],
                       key=str.lower))

            class_subclass_lvl_label[
                "text"] = f'\n{class_.name}s choose their {class_.subclass_name} at level {class_.subclass_lvl}, selecting from:\n\n{subclass_list}'

            resize_tabs()

    def skill_choosers(current_class):
        for chooser in class_skill_choosers_list:
            chooser.grid_forget()

        for n, option in enumerate(class_skill_choices):
            try:
                if current_class.skills[n] == "choose":
                    class_skill_choosers_list[n][
                        "postcommand"] = class_skill_chooser_prep
                    class_skill_choosers_list[n].grid(row=n + 1, pady=1, padx=4)
                else:
                    pass

                if option.get() not in [skill.name for skill in
                                        current_class.valid_skills]:
                    option.set("")
            except:
                option.set("")

    def class_skill_chooser_prep():

        chosen_skills = get_chosen_skills(character)

        current_class_instance.base_features()

        if isinstance(current_class_instance.valid_skills, str):
            valid_skills = [skill.key() for skill in skills_list]
        else:
            valid_skills = [skill.name for skill in
                            current_class_instance.valid_skills]

        for n, skill_chooser in enumerate(class_skill_choosers_list):
            current_chooser_choice = class_skill_choices[n].get()
            invalid_choices = chosen_skills.copy()
            invalid_choices.remove(current_chooser_choice)

            skills_options = [skill for skill in valid_skills if
                              skill not in invalid_choices]
            class_skill_choosers_list[n]["values"] = skills_options

    def equipment_selection(current_class):

        class equipment_selection:

            def __init__(self, index, choices):
                self.index = index
                self.tracking_variable = tk.IntVar()
                self.frame = tk.Frame(class_equipment_internal_frame)
                equipment_choices["selections"].append(self.tracking_variable)
                equipment_choices["selection_options"].append(choices)
                for i, options in enumerate(choices):
                    text = []
                    for j, item in enumerate(options):
                        if isinstance(item[0], tuple):
                            conditions = item[0]
                            # This assumes only two conditions, may prove to not be correct in the future but hey.
                            parent_1 = set(list(conditions[0].__bases__))
                            parent_2 = set(list(conditions[1].__bases__))

                            common_parent = list(parent_1.intersection(
                                parent_2))  # assume only one common parent

                            text_entry = f'{conditions[0].syntax_start(item[1])} {conditions[1].__name__} {common_parent[0].syntax_end(item[1])}'.lower()
                        elif item[0].__subclasses__():
                            text_entry = f'{item[0].syntax_start(item[1])} {item[0].__bases__[0].syntax_end(item[1])}'.lower()
                        else:
                            text_entry = item[0].syntax(item[1])

                        text.append(text_entry)

                    text = text_join(text, True, "")

                    button = tk.Radiobutton(self.frame,
                                            value=i,
                                            variable=self.tracking_variable,
                                            text=text,
                                            command=self.changed_selection)
                    button.grid(row=i, sticky=tk.W)
                    if i == 0:
                        button.select()

                    self.tracking_variable.trace("w",
                                                 self.changed_selection_auto)

                self.frame.update()

                self.frame.grid(row=index * 2, column=0, sticky=tk.W)
                ttk.Separator(class_equipment_internal_frame).grid(
                    row=index * 2 + 1, column=0, columnspan=3,
                    sticky=tk.EW)

            def changed_selection(self):
                get_choice_options(self.index)

            def changed_selection_auto(self, *args):
                self.tracking_variable
                get_choice_options(self.index)

        def get_choice_options(selection_index):
            current_selection_choice = equipment_choices["selections"][
                selection_index].get()

            current_selection_options = \
                equipment_choices["selection_options"][selection_index][
                    current_selection_choice]

            for child_widget in class_equipment_internal_frame.grid_slaves():
                if int(child_widget.grid_info()["column"]) > 0 and int(
                        child_widget.grid_info()["row"]) == 2 * selection_index:
                    for grandchild in child_widget.winfo_children():
                        grandchild.destroy()
                    child_widget.grid_forget()

            chooser_frame = tk.Frame(class_equipment_internal_frame)

            choices = []

            for option in current_selection_options:

                for n in range(option[1]):

                    if isinstance(option[0], tuple):

                        option_choice = tk.StringVar()
                        choices.append(option_choice)

                        conditions = option[0]
                        choice_options = ([condition.name for condition in
                                           conditions[0].__subclasses__() if
                                           issubclass(condition,
                                                      conditions[1])])

                        chooser = ttk.Combobox(chooser_frame,
                                               state="readonly",
                                               values=choice_options,
                                               textvariable=option_choice)
                        chooser.set(
                            f"Choose {conditions[0].__bases__[0].__name__.lower()}:")
                        chooser.pack(pady=2)

                    else:
                        if option[0].__subclasses__():
                            option_choice = tk.StringVar()
                            choices.append(option_choice)

                            choice_options = ([option.name for option in
                                               option[0].__subclasses__()])

                            chooser = ttk.Combobox(chooser_frame,
                                                   state="readonly",
                                                   values=choice_options,
                                                   textvariable=option_choice)
                            chooser.set(
                                f"Choose {option[0].__bases__[0].__name__.lower()}:")
                            chooser.pack(pady=2)

            chooser_frame.grid(row=selection_index * 2, column=1)

            equipment_choices["choices"][selection_index] = choices

            resize_tabs()

        for child_widget in class_equipment_internal_frame.winfo_children():
            child_widget.destroy()

        equipment_list = current_class.equipment

        equipment_choices = {"selections": [],
                             "selection_options": [],
                             "choices": []}

        num_selections = 0
        final_text = []
        final_equipment.pack_forget()

        for selection in equipment_list:
            num_options = len(selection)
            if num_options > 1:
                equipment_selection(num_selections, selection)
                equipment_choices["choices"].append([])
                get_choice_options(num_selections)
                num_selections += 1
            else:
                num_items = selection[0][1]
                final_text.append(selection[0][0]().syntax(num_items))

        final_equipment["text"] = text_join(final_text, True, "")
        final_equipment.pack(anchor="w")

        export_choices = equipment_choices.copy()
        del export_choices["selection_options"]

        character["equipment_choices"] = export_choices

    class_frame = tk.Frame(class_tab,
                           relief=tk.SUNKEN,
                           borderwidth=4)

    class_label = tk.Label(class_frame,
                           text="Class",
                           font=default_font + " 12 bold")

    class_label.pack(pady=8)

    class_choice_frame = tk.Frame(class_frame)
    class_choice_label = tk.Label(class_choice_frame,
                                  text="Choose starting class:",
                                  font=default_font + " 8")

    current_class_choice = tk.StringVar()
    class_choice_chooser = ttk.Combobox(class_choice_frame,
                                        values=list(class_list.keys()),
                                        state="readonly",
                                        textvariable=current_class_choice)

    class_choice_label.pack()
    class_choice_chooser.pack()
    class_choice_frame.pack()

    current_class_choice.trace("w", class_choice_changed)

    class_info_frame = tk.Frame(class_frame)

    class_top_label = tk.Label(class_info_frame,
                               font=default_font + " 10 bold")

    class_description = tk.StringVar()

    class_description_label = tk.Label(class_info_frame,
                                       textvariable=class_description,
                                       font=default_font + " 8",
                                       wraplength=640)
    class_description_label.pack(pady=8)

    class_features_internal_frame = tk.Frame(class_info_frame)

    class_left_frame = tk.Frame(class_features_internal_frame)

    class_basic_info_text = tk.Label(class_left_frame,
                                     font=default_font + " 8",
                                     justify=tk.CENTER,
                                     wraplength=160
                                     )

    class_basic_info_label = tk.Label(class_left_frame,
                                      text="Class Info:",
                                      font=default_font + " 8 bold")

    class_basic_info_label.pack()
    class_basic_info_text.pack()

    class_divider_1 = ttk.Separator(class_features_internal_frame,
                                    orient=tk.VERTICAL)

    class_divider_2 = ttk.Separator(class_features_internal_frame,
                                    orient=tk.VERTICAL)

    class_central_frame = tk.Frame(class_features_internal_frame)

    class_primary_attributes = tk.StringVar()

    class_skills_frame = tk.Frame(class_central_frame)

    class_skills_label = tk.Label(class_skills_frame,
                                  text="Class Skills:",
                                  font=default_font + " 8 bold"
                                  )

    class_skills_choosers_frame = tk.Frame(class_skills_frame)

    class_skills_chooser_label = tk.Label(class_skills_choosers_frame,
                                          text="Choose skill proficiencies:",
                                          font=default_font + " 8")

    class_skill_1 = tk.StringVar()
    class_skill_2 = tk.StringVar()
    class_skill_3 = tk.StringVar()
    class_skill_4 = tk.StringVar()

    class_skill_chooser_1 = ttk.Combobox(class_skills_choosers_frame,
                                         state="readonly",
                                         textvariable=class_skill_1)
    class_skill_chooser_2 = ttk.Combobox(class_skills_choosers_frame,
                                         state="readonly",
                                         textvariable=class_skill_2)
    class_skill_chooser_3 = ttk.Combobox(class_skills_choosers_frame,
                                         state="readonly",
                                         textvariable=class_skill_3)
    class_skill_chooser_4 = ttk.Combobox(class_skills_choosers_frame,
                                         state="readonly",
                                         textvariable=class_skill_4)

    class_skill_choosers_list = [class_skill_chooser_1, class_skill_chooser_2,
                                 class_skill_chooser_3,
                                 class_skill_chooser_4]
    class_skill_choices = [class_skill_1, class_skill_2, class_skill_3,
                           class_skill_4]

    for n, skill_choice in enumerate(class_skill_choices):
        name = f'Class Skill {n + 1}'
        character[name] = skill_choice

    class_skills_chooser_label.grid(row=0)
    class_skill_chooser_1.grid(row=1, pady=1, padx=4)
    class_skill_chooser_2.grid(row=2, pady=1)
    class_skill_chooser_3.grid(row=3, pady=1)
    class_skill_chooser_4.grid(row=4, pady=1)

    class_skills_label.pack()
    class_skills_frame.pack()
    class_skills_choosers_frame.pack()

    class_subclass_lvl_frame = tk.Frame(class_central_frame)
    class_subclass_lvl_label = tk.Label(class_subclass_lvl_frame,
                                        font=default_font + " 8",
                                        wraplength=200)
    class_subclass_lvl_label.pack()
    class_subclass_lvl_frame.pack()

    class_right_frame = tk.Frame(class_features_internal_frame)

    class_equipment_frame = tk.Frame(class_right_frame)

    tk.Label(class_equipment_frame,
             text="Class Equipment:",
             font=default_font + " 8 bold").pack()

    tk.Label(class_equipment_frame,
             text="You recieve the following items, plus any provided by your background:",
             font=default_font + " 8",
             wraplength=220).pack()

    class_equipment_internal_frame = tk.Frame(class_equipment_frame)

    class_equipment_frame.pack()
    class_equipment_internal_frame.pack(fill="x", expand=True)

    final_equipment = tk.Label(class_equipment_frame,
                               justify=tk.LEFT)

    class_info_frame.pack()
    class_top_label.pack()
    class_features_internal_frame.pack()

    class_data = {"Class Choice": class_choice_chooser}

    character.update(class_data)

    class_label.pack()

    return class_frame


def Background_():
    def changed_background(*args):
        background_choice_instance = background_list[background_choice.get()]()

        background_name_text_var.set(background_choice_instance.name)

        background_desc_text.delete('1.0', tk.END)
        background_desc_text.insert(tk.END, background_choice_instance.feature)

        # Check text height and adjust box
        text_height = (len(textwrap.wrap(background_choice_instance.feature,
                                         background_desc_text['width']))
                       + background_choice_instance.feature.count("\n"))
        background_desc_text['height'] = text_height

        background_desc_text.update()

        background_name_text.pack()
        background_desc_text.pack(pady=4)

        resize_tabs()

    background_frame = tk.Frame(background_tab,
                                relief=tk.SUNKEN,
                                borderwidth=4,
                                )

    background_label = tk.Label(background_frame,
                                text="Background",
                                font=default_font + " 12 bold")

    background_label.pack(pady=8)

    background_chooser_frame = tk.Frame(background_frame)

    background_chooser_label = tk.Label(background_chooser_frame,
                                        text="Choose background template:\n"
                                             "(Name and description can be "
                                             "altered if desired)",
                                        font=default_font + " 8")

    background_choice = tk.StringVar()
    background_choice.trace("w", changed_background)
    background_chooser = ttk.Combobox(background_chooser_frame,
                                      state='readonly',
                                      values=[bg.name for bg in
                                              Background.__subclasses__()],
                                      textvariable=background_choice)

    background_chooser_label.pack()
    background_chooser.pack()
    background_chooser_frame.pack()

    background_features_frame = tk.Frame(background_frame)
    background_name_text_var = tk.StringVar()
    background_name_text = tk.Entry(background_features_frame,
                                    textvariable=background_name_text_var,
                                    justify="center")

    background_desc_text = tk.Text(background_features_frame,
                                   height=10,
                                   width=80,
                                   wrap=tk.WORD)

    background_features_frame.pack(pady=8)

    background_features_dict = {'background_choice': background_chooser}

    return background_frame


window = tk.Tk()
window.title("Character Creator")
default_font = "Verdana"

# Character Creation Stuff

character_creator = tk.Frame(window)

tab_manager = ttk.Notebook(character_creator)

info_tab = ttk.Frame(tab_manager,
                     relief=tk.FLAT,
                     borderwidth=5)
race_tab = ttk.Frame(tab_manager,
                     relief=tk.FLAT,
                     borderwidth=5)
class_tab = ttk.Frame(tab_manager,
                      relief=tk.FLAT,
                      borderwidth=5)

background_tab = ttk.Frame(tab_manager,
                           relief=tk.FLAT,
                           borderwidth=5)

tab_manager.add(info_tab, text="Info")

tab_manager.add(race_tab, text="Race")

tab_manager.add(class_tab, text="Class")

tab_manager.add(background_tab, text="Background")


def change_tabs(event):
    event.widget.update_idletasks()
    current_tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(height=current_tab.winfo_reqheight(),
                           width=current_tab.winfo_reqwidth())

    character_creator.update_idletasks()
    tab_manager.update_idletasks()
    if character_creator.winfo_width() > tab_manager.winfo_reqwidth():
        tab_manager.configure(width=character_creator.winfo_width())

        current_tab_contents = \
            tab_manager.nametowidget(tab_manager.select()).winfo_children()[0]

        current_tab_contents.pack(fill="both", expand=True)


def resize_tabs():
    tab_manager.update_idletasks()
    current_tab = tab_manager.nametowidget(tab_manager.select())
    tab_manager.configure(height=current_tab.winfo_reqheight(),
                          width=current_tab.winfo_reqwidth())


tab_manager.bind("<<NotebookTabChanged>>", change_tabs)

character = {}

Title()

Info().pack()
Class().pack()
Race().pack()
Background_().pack()

tab_manager.pack()
character_creator.pack()

style = ttk.Style(window)
style.configure('TNotebook', tabposition='n')

# Move window to centre

windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
position_right = int(window.winfo_screenwidth() / 3 - windowHeight / 2)
position_down = int(window.winfo_screenheight() / 4 - windowHeight / 2)
window.geometry(f"+{position_right}+{position_down}")

window.mainloop()
