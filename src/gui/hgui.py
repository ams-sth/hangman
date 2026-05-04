import customtkinter as ctk

from gui.menuscreen import MenuScreen
from gui.gamescreen import GameScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HangmanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman")
        self.master.geometry("600x500")
        self.master.resizable(True, True)

        self.current_screen = None
        self._theme = "dark" 
        self.show_menu()

    def toggle_theme(self):
        cycle = {"dark": "light", "light": "system", "system": "dark"}
        self._theme = cycle[self._theme]
        ctk.set_appearance_mode(self._theme)

    def show_menu(self):
        self._clear()
        self.current_screen = MenuScreen(self.master, on_start=self.show_game, on_toggle_theme=self.toggle_theme, current_theme=self._theme)
        self.current_screen.pack(expand=True, fill="both")

    def show_game(self, level):
        self._clear()
        self.current_screen = GameScreen(
            self.master,
            level=level,
            on_new_game=self.show_menu,
            current_theme=self._theme,        
            on_toggle_theme=self.toggle_theme
        )
        self.current_screen.pack(expand=True, fill="both")

    def _clear(self):
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None