import customtkinter as ctk

class ThemeToggleButton(ctk.CTkButton):
    ICONS = {"dark": "☀️", "light": "🌙", "system": "⚙️"}
    CYCLE = {"dark": "light", "light": "system", "system": "dark"}

    def __init__(self, master, current_theme, on_toggle):
        self._current_theme = current_theme
        self._on_toggle = on_toggle
        super().__init__(
            master,
            text=self.ICONS[current_theme],
            width=40, height=40,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            command=self._toggle
        )

    def _toggle(self):
        self._current_theme = self.CYCLE[self._current_theme]
        self.configure(text=self.ICONS[self._current_theme])
        self._on_toggle()