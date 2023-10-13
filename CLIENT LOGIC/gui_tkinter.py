"""
BPMI Pipe Cleaning and Inspection Robot
File Name: gui_tkinter.py
Date Created: 10/11/2023 SAT
Date Last Modified: 10/11/2023 SAT
Description: gui code for tkinter implementation
Verion: 0.0.1
Authors: Tiwari, Gomez, Bennett

Build Notes: Initial structure and research

Dependencies: None

References:
https://docs.python.org/3/library/tkinter.html

Additional Notes:

"""

import tkinter as tk
from main_pc import startup

def start_button():
    startup()

window = tk.Tk()
window.title("BPMI Robot Control")


power_button = tk.Button(window, text="Start Robot", command=start_button)
power_button.pack()

window.mainloop()