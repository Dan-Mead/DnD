import tkinter as tk
from tkinter import ttk
from addict import Dict
import pickle


def export(character):
    name = character["Name"]

    if name == "":
        name = "Test_Character"

    loc = f'saves/{name}'

    with open(loc + '.pkl', "wb") as file:
        pickle.dump(character, file, pickle.HIGHEST_PROTOCOL)
    file.close()

    return name


def import_info():
    name = "Test_1"

    loc = f'saves/{name}.pkl'

    file = open(loc, "rb")
    info = pickle.load(file)
    file.close()

    return info

    # for key, value in form_data[middle_frame_index].items():
    #     text = character[key]
    #     value.insert(0, text)


def update_character_info(index):

    data = form_data[index]

    for key in data:
        try:
            character[key] = data[key].get()
        except:
            pass



def save():
    name = export(character)
    return name

def Title():
    title = tk.Label(master=character_creation_frame,
                     text='Character Creation',
                     bd=8,
                     font=default_font + " 16 bold")

    title.pack(side=tk.TOP)


def Buttons():
    buttons = tk.Frame(master=character_creation_frame)

    def close():
        global middle_frame_index

        update_character_info(middle_frame_index)

        save()
        window.destroy()

    close_button = tk.Button(master=buttons,
                             text="Close",
                             command=close)

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

    next_button = tk.Button(master=buttons,
                            text="Next",
                            command=next)

    back_button = tk.Button(master=buttons,
                            text="Back",
                            command=back)

    close_button.grid(row=0, column=1)
    next_button.grid(row=0, column=2)

    buttons.pack(side=tk.BOTTOM)

def Info(index):
    info_frame = tk.Frame(master=character_creation_frame,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )

    ### Character Name

    name_frame = tk.Frame(master=info_frame)

    name_label = tk.Label(master=name_frame,
                          text='Character name',
                          font=default_font + " 12 bold")
    name_entry = tk.Entry(master=name_frame,
                          width=24,
                          justify="center")

    name_label.pack()
    name_entry.pack()

    name_frame.pack(padx=8, pady=(8, 16))

    ### Character info

    data_frame = tk.Frame(master=info_frame)

    #### Age

    age_frame = tk.Frame(master=data_frame)

    age_label = tk.Label(master=age_frame,
                         text="Age",
                         font=default_font + " 10")
    age_entry = tk.Entry(master=age_frame,
                         width=8,
                         justify="center")

    age_label.grid(row=0)
    age_entry.grid(row=1)

    #### Gender

    gender_frame = tk.Frame(master=data_frame)

    gender_label = tk.Label(master=gender_frame,
                            text="Gender",
                            font=default_font + " 10")
    gender_entry = tk.Entry(master=gender_frame,
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

    appearance_frame = tk.Frame(master=data_frame)
    size_frame = tk.Frame(master=data_frame)

    physicals = {}

    row = 0
    for j in range(len(appearance_aspects)):

        frames = appearance_frame, size_frame
        aspects = appearance_aspects, size_aspects

        for k, frame in enumerate(frames):
            label = tk.Label(master=frame,
                             text=aspects[k][j],
                             font=default_font + " 10")
            entry = tk.Entry(master=frame,
                             width=8,
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

    faith_frame = tk.Frame(master=info_frame)

    faith_label = tk.Label(master=faith_frame,
                           text='Faith',
                           font=default_font + " 10")
    faith_entry = tk.Entry(master=faith_frame,
                           width=16,
                           justify="center")

    faith_label.pack()
    faith_entry.pack()

    faith_frame.pack(pady=2)

    ### Alignment

    alignment_frame = tk.Frame(master=info_frame)

    alignment_label = tk.Label(master=faith_frame,
                               text='Alignment',
                               font=default_font + " 10")

    alignment_entry_frame = tk.Frame(master=alignment_frame)

    ethics = ttk.Combobox(master=alignment_entry_frame,
                          values=["Lawful", "Neutral", "Chaotic"],
                          state="readonly",
                          width=8)
    morality = ttk.Combobox(master=alignment_entry_frame,
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
    race_frame = tk.Frame(master=character_creation_frame,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )
    race_label = tk.Label(master=race_frame,
                          text="Race!")

    race_data = {"Race": "Race Data"}

    form_data[index] = race_data

    race_label.pack()

    return race_frame

def Class(index):
    class_frame = tk.Frame(master=character_creation_frame,
                          relief=tk.SUNKEN,
                          borderwidth=4,
                          )
    class_label = tk.Label(master=class_frame,
                          text="Class")

    class_data = {"Class": "Class Data"}

    form_data[index] = class_data

    class_label.pack()

    return class_frame


window = tk.Tk()

default_font = "Verdana"

# Character Creation Stuff

character_creation_frame = tk.Frame(master=window,
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
page_number_text.set(f'Page {middle_frame_index+1} of {len(middle_frames)}')

page_number = tk.Label(master=character_creation_frame, textvariable=page_number_text)
page_number.pack()
Buttons()

# Packing Main Page

character_creation_frame.pack()

window.mainloop()
