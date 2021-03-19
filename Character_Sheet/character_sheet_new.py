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

from Character_Sheet.character import Character, ExportDict
from Character_Sheet.reference.items import *
import Character_Sheet.helpers as helpers
import Character_Sheet.reference.skills_and_attributes as skills
import Character_Sheet.reference.glossary as glossary

default_font = "Verdana"



def startup(load=None):
    global window, char

    window = tk.Tk()
    char = Character()

    # char.load(filename, type)

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