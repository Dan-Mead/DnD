import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from functools import partial
import textwrap
import num2words

def import_info(filename):
    file = open(filename, "rb")
    info = pickle.load(file)
    file.close()
    return info

class Character:
    def __init__(self):
        pass

    def load(self):
        filename = tk.filedialog.askopenfilename(initialdir="saves/",
                                                 title="Select save file",
                                                 filetypes=(
                                                     ("Pickled Files", "*.pkl"),
                                                     ("all files", "*.*")))

        character_import_dict = import_info(filename)
        for key, value in character_import_dict.items():
            setattr(self, key.lower(), value)
            print(key, value)
        # for condition in range(num_layers):
        #     for key, value in character_import_dict.items():
