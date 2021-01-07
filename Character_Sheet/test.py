import tkinter as tk

window = tk.Tk()

frame_1 = tk.Frame(window)
tk.Label(frame_1,
         text="Frame 1").pack()

frame_1.grid(row=0,column=0, padx=4)

frame_2 = tk.Frame(window)
tk.Label(frame_2,
         text="Frame 2").pack()

frame_2.grid(row=0, column=1, padx=4)

test_label = tk.Label(master=frame_1,
                      text="Test is here")

test_label.configure(master=frame_2)



test_label.pack()

window.mainloop()
