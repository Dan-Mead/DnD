import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from addict import Dict
import pickle

from races import race_list
from glossary import common_languages, exotic_languages, attrs


def export(character):
    name = character["Name"]

    if name == "":
        name = "Test_Character"

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

    row = 0
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

            label.grid(row=row * 2, pady=(2, 1))
            entry.grid(row=row * 2 + 1)

        row += 1

    ### Add all data to frame

    age_frame.grid(row=0, column=0, padx=(0, 8), pady=(0, 10))
    gender_frame.grid(row=0, column=1, padx=(8, 0), pady=(0, 10))
    appearance_frame.grid(row=1, column=0, padx=(0, 8))
    size_frame.grid(row=1, column=1, padx=(8, 0))

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
        choice = race_choice.get()

        size = race_list[choice].size
        speed = race_list[choice].speed
        race_size_text.set(size)
        race_speed_text.set(f'{speed} ft.')

        if race_list[choice].__subclasses__():
            subrace_choice.pack()
            subrace_choice.set("Choose subrace: ")
            asi_frame.pack_forget()
            subclass = True

        else:
            subrace_choice.pack_forget()
            subclass = False

        race_info.pack_forget()
        race_info.pack()
        race_languages_choice.grid_forget()
        race_base_info.update()
        languages(choice)

        if subclass == False:
            ASI(choice, None)
            other_features(choice, None)

    def languages(choice):

        language_list = [language for language in race_list[choice].languages]

        choices_num = language_list.count("Choice")

        if choices_num > 0:
            language_list.remove("Choice")
            race_languages_choice.grid(row=3, column=2, stick="W")

            divider.grid(rowspan=race_base_info.grid_size()[1])

            known_languages = language_list
            language_choices = ["None"] + common_languages + exotic_languages
            for lang in known_languages:
                language_choices.remove(lang)
            race_languages_choice["values"] = language_choices

        language_list = "\n".join(language_list)

        race_language_text.set(language_list)

    def ASI(race, subrace):

        if subrace == None:

            ASI = race_list[race].ASI

        else:
            subraces_list = dict([(subrace.subrace_name, subrace) for subrace in race_list[race].__subclasses__()])

            ASI = subraces_list[subrace].ASI

        num_choices = 0
        choice_options = []

        for i in ASI:
            if i[0] == "Choice":
                num_choices += 1
                choice_options.append(i[1])

        ASI_automatic = dict(ASI)

        if num_choices > 0:
            del ASI_automatic["Choice"]

        for asi_value in asi_automatic_values:
            asi_value.configure(text="")

        for attribute, attr_value in ASI_automatic.items():
            attr_index = attrs.index(attribute)

            text_value = f'{attr_value:+d}'

            asi_automatic_values[attr_index].configure(text=text_value)

        asi_choice_1.grid_forget()
        asi_choice_2.grid_forget()

        if num_choices > 0:
            asi_choice_1.grid(row=7, column=0, columnspan=3)
            if choice_options[0] == "Any":
                asi_options = attrs.copy()
            else:
                asi_options = attrs.copy()
                asi_options.remove(choice_options[0])

            asi_choice_1_val = tk.StringVar()
            asi_choice_1["textvariable"] = asi_choice_1_val
            asi_choice_1["values"] = asi_options
        if num_choices == 2:
            asi_choice_2.grid(row=8, column=0, columnspan=3)

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



        asi_frame.pack()

    def other_features(race, subrace):
        pass

    ## Main Code

    race_frame = tk.Frame(character_creation_frame,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )
    race_label = tk.Label(race_frame,
                          text="Race",
                          font=default_font + " 12 bold")

    current_race = tk.StringVar()

    race_choice = ttk.Combobox(race_frame,
                               values=[race for race in race_list],
                               state="readonly",
                               width=16,
                               textvariable=current_race)

    race_choice.set("Choose race: ")

    current_subrace = tk.StringVar()

    def get_subclasses():
        choice = race_choice.get()
        subrace_choice["values"] = [subrace.subrace_name for subrace in race_list[choice].__subclasses__()]

    subrace_choice = ttk.Combobox(race_frame,
                                  postcommand=get_subclasses,
                                  values=[],
                                  state="readonly",
                                  width=16,
                                  textvariable=current_subrace)

    race_info = tk.Frame(race_frame)

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

    ttk.Separator(race_base_info).grid(column=0, row=5, columnspan=3, sticky="EW")

    race_base_info.pack()

    def subrace_chosen(event):
        ASI(race_choice.get(), subrace_choice.get())

    subrace_choice.bind("<<ComboboxSelected>>", subrace_chosen)

    def changed_race(*args):
        current_race  # this is essential and I have no idea why, even pycharm says it seems to do nothing
        update_race_info()

    current_race.trace('w', changed_race)

    asi_frame = tk.Frame(race_info)
    asi_automatic_values = [None] * 6
    for n, attribute in enumerate(attrs):
        label = tk.Label(asi_frame,
                         text=attribute,
                         font=default_font + " 10 bold")
        label.grid(row=n, column=0, sticky="E")

        value = tk.Label(asi_frame,
                         font=default_font + " 10")

        value.grid(row=n, column=2, sticky="W")
        asi_automatic_values[n] = value

    ttk.Separator(asi_frame,
                  orient=tk.VERTICAL) \
        .grid(column=1, row=0, sticky="NS", rowspan=asi_frame.grid_size()[1])


    asi_choice_1 = ttk.Combobox(asi_frame,
                                state="readonly",
                                width=12)

    asi_choice_2 = ttk.Combobox(asi_frame,
                                state="readonly",
                                width=12)

    asi_choice_1.grid(row=7, column=0, columnspan=3)
    asi_choice_2.grid(row=8, column=0, columnspan=3)

    race_data = {"Race": race_choice,
                 "Subrace": subrace_choice,
                 "Languages": race_languages_choice
                 }

    form_data[index] = race_data

    race_label.pack(pady=(8, 8))
    race_choice.pack()

    return race_frame


def Class(index):
    class_frame = tk.Frame(character_creation_frame,
                           relief=tk.SUNKEN,
                           borderwidth=4,
                           )
    class_label = tk.Label(class_frame,
                           text="Class")

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
