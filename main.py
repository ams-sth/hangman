import sys
import os
sys.path.insert(0, os.path.abspath("src"))

import customtkinter as ctk
from gui.hgui import HangmanGUI

if __name__ == "__main__":
    root = ctk.CTk()
    app = HangmanGUI(root)
    root.mainloop()