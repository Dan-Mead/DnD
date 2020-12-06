import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pickle

from Character_Sheet.reference.races import race_list
from Character_Sheet.reference.feats import feat_list, unpack_desc
from Character_Sheet.reference.glossary import common_languages, exotic_languages, attrs, skills_dict


global current_race_instance, current_subrace_instance


def export(character):
    name = character["Name"]

    if name == "":
        name = "Empty_Character"

    loc = f'saves/{name}'

    with open(loc + '.pkl', "wb") as file:
        pickle.dump(character, file, pickle.HIGHEST_PROTOCOL)
    file.close()


def import_info(filename):
    # name = "Test_1"

    # loc = f'saves/{name}.pkl'

    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()

    return info


def update_character_info(index):
    data = form_data[index]

    for key in data:
        try:
            character[key] = data[key].get()
        except:
            pass


def save():
    update_character_info(middle_frame_index)
    export(character)


def load():
    filename = tk.filedialog.askopenfilename(initialdir="saves/",
                                             title="Select save file",
                                             filetypes=(("Pickled Files", "*.pkl"),
                                                        ("all files", "*.*")))

    character = import_info(filename)

    for sheet in form_data:
        for key, value in sheet.items():
            text = character[key]
            if isinstance(value, tk.ttk.Combobox):
                # value["state"] = "normal"
                # value.delete(0, tk.END)
                # value.insert(0, text)
                # value["state"] = "readonly"
                value.set(text)
            else:
                value.delete(0, tk.END)
                value.insert(0, text)


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
    exit_label = tk.Label(exit_window, text="Would you like to save?", font=default_font + " 10")
    exit_label.pack()
    exit_buttons = tk.Frame(exit_window)
    yes_button = tk.Button(exit_buttons, width=8, text="Yes", command=exit_save_and_close)
    no_button = tk.Button(exit_buttons, width=8, text="No", command=exit_close)
    cancel_button = tk.Button(exit_buttons, width=8, text="Cancel", command=exit_window.destroy)

    yes_button.grid(row=1, column=0, padx=4)
    no_button.grid(row=1, column=1, padx=4, pady=8)
    cancel_button.grid(row=1, column=2, padx=4)

    exit_buttons.pack()

    # window.destroy()


def Title():
    title = tk.Label(character_creation_frame,
                     text='Character Creation',
                     bd=8,
                     font=default_font + " 16 bold")

    title.pack(side=tk.TOP)

    main_menu = tk.Menu(character_creation_frame)

    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Save", command=save)
    file_menu.add_command(label="Load", command=load)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit)
    main_menu.add_cascade(label="File", menu=file_menu)

    window.config(menu=main_menu)


def Buttons():
    buttons = tk.Frame(character_creation_frame)

    def back():

        global middle_frame_index

        update_character_info(middle_frame_index)

        middle_frames[middle_frame_index].pack_forget()

        middle_frame_index -= 1
        page_number_text.set(f'Page {middle_frame_index + 1} of {len(middle_frames)}')

        middle_frames[middle_frame_index].pack(fill=tk.X)
        page_number.pack_forget()
        page_number.pack()

        if middle_frame_index < len(middle_frames) - 1:
            next_button.grid(row=0, column=2)

        if middle_frame_index == 0:
            back_button.grid_forget()

    def next():

        global middle_frame_index

        update_character_info(middle_frame_index)

        middle_frames[middle_frame_index].pack_forget()

        middle_frame_index += 1
        page_number_text.set(f'Page {middle_frame_index + 1} of {len(middle_frames)}')

        middle_frames[middle_frame_index].pack(fill=tk.X)
        page_number.pack_forget()
        page_number.pack()

        if middle_frame_index > 0:
            back_button.grid(row=0, column=0)

        if middle_frame_index == len(middle_frames) - 1:
            next_button.grid_forget()

    close_button = tk.Button(buttons,
                             text="Close",
                             command=exit,
                             width=6)

    next_button = tk.Button(buttons,
                            text="Next",
                            command=next,
                            width=6)

    back_button = tk.Button(buttons,
                            text="Back",
                            command=back,
                            width=6)

    close_button.grid(row=0, column=1, padx=8)
    next_button.grid(row=0, column=2)

    buttons.update()
    sizes = [close_button.winfo_width(), next_button.winfo_width()]
    buttons.grid_columnconfigure((0, 1, 2), minsize=max(sizes))

    buttons.pack(side=tk.BOTTOM)


def Info(index):
    info_frame = tk.Frame(character_creation_frame,
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

    form_data[index] = character_info

    return info_frame


def Race(index):
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

        language_list = [language for language in current_race_instance.languages]

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

        bottom_divider.grid(column=0, row=5, columnspan=3, sticky="EW", pady=(4, 0))

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
                attr_index = attrs.index(attribute)

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
            asi_choice_label["text"] = "Choose ability scores to increase by +1:"
            asi_choice_2.grid(row=2)
            asi_choice_2_val = tk.StringVar()
            asi_choice_2["textvariable"] = asi_choice_2_val

            def check_asi_1_choices():
                second_choice = asi_choice_2.get()
                if not (second_choice):
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

        if current_subrace_instance:
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

        form_data[index] = race_data
        update_character_info(index)

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

        if isinstance(valid_skills, str):
            skills_reference_dict = skills_dict.copy()
            if valid_skills == "any":
                valid_skills_name_list = tuple([value[0] for value in skills_reference_dict.values()])
            else:
                valid_skills_name_list = tuple([skills_reference_dict[skill][0] for skill in valid_skills])

            skill_chooser_1["postcommand"] = None
            skill_chooser_1["text_variable"] = None
            skill_chooser_2["postcommand"] = None
            skill_chooser_2["text_variable"] = None
            skill_chooser_2.set("")
            skill_chooser_1["values"] = valid_skills_name_list
            skill_chooser_1.set("")
            skill_chooser_2.pack_forget()

        else:
            def choose_race_skill():
                for n, options in enumerate(valid_skills):
                    skills_reference_dict = skills_dict.copy()
                    if options == "any":
                        valid_skills_name_list = tuple([skill[0] for skill in skills_reference_dict.values()])
                    else:
                        valid_skills_name_list = tuple([skills_reference_dict[skill][0] for skill in options])

                    other_skills_chosen = skills_choices.copy()
                    del other_skills_chosen[n]

                    final_skill_list = list(valid_skills_name_list).copy()

                    for chosen in other_skills_chosen:
                        chosen = chosen.get()
                        if chosen in final_skill_list:
                            final_skill_list.remove(chosen)

                    race_skill_choosers[n]["values"] = final_skill_list

            race_skill_choosers = [skill_chooser_1, skill_chooser_2]  # TODO: this is a set size, not good
            skills_choices = [tk.StringVar(), tk.StringVar()]
            for n, skill_chooser in enumerate(race_skill_choosers):

                if valid_skills[n] == "any" or skill_chooser.get() in valid_skills[n]:
                    skills_choices[n].set(skill_chooser.get())
                skill_chooser["textvariable"] = skills_choices[n]
                skill_chooser["postcommand"] = choose_race_skill
                skill_chooser.pack()

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
    race_frame = tk.Frame(character_creation_frame,
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
        subrace_choice["values"] = [subrace.subrace_name for subrace in current_race_instance.__subclasses__()]

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

    divider.grid(column=1, row=0, rowspan=race_base_info.grid_size()[1], sticky="NS")

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

    current_race.trace('w', changed_race)

    def changed_subrace(*args):
        global current_subrace_instance
        if race_list[current_race.get()].__subclasses__() and current_subrace.get() != subrace_choice_prompt:
            current_subrace_instance = \
                {subrace.subrace_name: subrace for subrace in current_race_instance.__subclasses__()}[
                    current_subrace.get()]
            asi_frame.grid_forget()
            bottom_divider.grid_forget()
            ASI()
            other_features()

        elif current_subrace.get() == subrace_choice_prompt:
            race_features_frame.grid_forget()
            current_subrace_instance = None

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
                  orient=tk.VERTICAL).grid(column=1, row=0, sticky="NS", rowspan=asi_attributes_frame.grid_size()[1])

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
    skill_chooser_1 = ttk.Combobox(skill_chooser_frame,
                                   state="readonly")
    skill_chooser_label.pack(pady=(4, 0))
    skill_chooser_1.pack()

    skill_chooser_2 = ttk.Combobox(skill_chooser_frame,
                                   state="readonly")
    skill_chooser_2.pack()

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

            feature_value = current_race_instance.choice_features[race_feature_chosen.get()]

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

    def subrace_feature_changed(*args):
        if subrace_feature_chosen.get():

            feature_value = current_subrace_instance.choice_features[subrace_feature_chosen.get()]

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
                 "ASI choice 1": asi_choice_1,
                 "ASI choice 2": asi_choice_2,
                 "race_skill 1": skill_chooser_1,
                 "race skill 2": skill_chooser_2,
                 "race_feat": feat_chooser,
                 "race_feature": race_feature_chooser,
                 "subrace_feature": subrace_feature_chooser
                 }

    form_data[index] = race_data

    return race_frame


def Class(index):
    class_frame = tk.Frame(character_creation_frame,
                           relief=tk.SUNKEN,
                           borderwidth=4,
                           )
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
                                        values=["Classes"],
                                        textvariable = current_class_choice)

    class_choice_label.pack()
    class_choice_chooser.pack()
    class_choice_frame.pack()

    class_data = {"Class": "Class Data"}

    form_data[index] = class_data

    class_label.pack()

    return class_frame


window = tk.Tk()

default_font = "Verdana"

# Character Creation Stuff

character_creation_frame = tk.Frame(window,
                                    relief=tk.FLAT,
                                    borderwidth=5)

## Frames list

middle_frames = [Info,
                 Race,
                 Class]

form_data = [None] * len(middle_frames)

for n, frame in enumerate(middle_frames):
    middle_frames[n] = frame(n)
    middle_frames[n].pack_forget()

character = {}

## Packing Character Creation

Title()
middle_frame_index = 0
middle_frames[middle_frame_index].pack(fill=tk.X)

page_number_text = tk.StringVar()
page_number_text.set(f'Page {middle_frame_index + 1} of {len(middle_frames)}')

page_number = tk.Label(character_creation_frame, textvariable=page_number_text)
page_number.pack()
Buttons()

# Packing Main Page

character_creation_frame.pack()

window.mainloop()
