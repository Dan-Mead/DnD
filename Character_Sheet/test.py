import tkinter as tk
from tkinter import ttk

window = tk.Tk()

notebook = ttk.Notebook(window)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="First Tab")
notebook.add(tab2, text="First Tab")

tk.Label(tab1, text = "Test Sucessful").pack()

notebook.pack()

window.mainloop()
