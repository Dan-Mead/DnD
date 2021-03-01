import os
import pickle, pickle5
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path


from functools import partial
import textwrap
import num2words
import math

import Character_Sheet.helpers as helpers
import Character_Sheet.reference.glossary as glossary
import Character_Sheet.reference.races as races
import Character_Sheet.reference.classes as classes
import Character_Sheet.reference.items as items
import Character_Sheet.reference.backgrounds as backgrounds
import Character_Sheet.reference.skills_and_attributes as skills

class Character:

    class Updatable:
        values = []

        @classmethod
        def update_all(cls):

    def load(self):
        pass

    def save(self):
        pass

    def __init__(self):
        pass



if __name__ == "__main__":
    window = tk.Tk()
    char = Character()