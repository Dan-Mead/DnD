import tkinter as tk
from tkinter import ttk

window = tk.Tk()

button_choice = tk.IntVar()
tk.Radiobutton(window,
               variable=button_choice,
               value=1,
               text="Option1").pack()
tk.Radiobutton(window,
               variable=button_choice,
               value=0,
               text="Option2").pack()


window.mainloop()
