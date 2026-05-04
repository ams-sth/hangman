import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from gui.hgui import HangmanApp


import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = HangmanApp(root)
    root.mainloop()