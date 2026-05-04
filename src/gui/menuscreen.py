import customtkinter as ctk
from gui.widgets import ThemeToggleButton

class MenuScreen(ctk.CTkFrame):
    def __init__(self, master, on_start, on_toggle_theme, current_theme):
        super().__init__(master, fg_color="transparent")
        self.on_start = on_start
        self.on_toggle_theme = on_toggle_theme
        self.current_theme = current_theme
        self._build()

    def _build(self):
        ThemeToggleButton(
            self,
            current_theme=self.current_theme,
            on_toggle=self.on_toggle_theme
        ).place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        ctk.CTkLabel(
            self,
            text="Hangman",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self,
            text="Select Level:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        self.level_var = ctk.StringVar(value="basic")

        ctk.CTkOptionMenu(
            self,
            variable=self.level_var,
            values=["basic", "intermediate"],
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Start Game",
            command=self._start,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Note: You can use the Keyboard!",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=10)

    def _start(self):
        self.on_start(self.level_var.get())