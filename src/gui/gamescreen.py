import customtkinter as ctk
from PIL import Image

from gui.dialogs import GameDialog
from gui.widgets import ThemeToggleButton
from logic.hlogic import HangmanLogic


class GameScreen(ctk.CTkFrame):
    def __init__(self, master, level, on_new_game, current_theme, on_toggle_theme):
        super().__init__(master, fg_color="transparent")
        self.level = level
        self.on_new_game = on_new_game
        self.on_toggle_theme = on_toggle_theme
        self.current_theme = current_theme
        self.game = HangmanLogic(level=self.level)
        self.time_left = 15

        self._load_images()
        self._build()
        self._bind_keys()
        self.update_display()
        self.start_timer()

    def _load_images(self):
        paths = [f"images/hangman{i}.png" for i in range(6, -1, -1)]
        try:
            self.images = [
                ctk.CTkImage(
                    light_image=Image.open(p).resize((200, 200)),
                    dark_image=Image.open(p).resize((200, 200)),
                    size=(200, 200)
                ) for p in paths
            ]
        except Exception:
            self.images = [None] * 7

    def _bind_keys(self):
        self.master.bind("<Key>", self._handle_keypress)

    def _build(self):
        self._build_status_bar()
        self._build_main_area()
        self._build_letter_buttons()

    def _build_status_bar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=(20, 10))

        self.timer_label = ctk.CTkLabel(
            bar, text="Time left: 15s",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("red", "#ff6b6b")
        )
        self.timer_label.grid(row=0, column=0, padx=5)

        ctk.CTkLabel(
            bar, text=f"Level: {self.level.capitalize()}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("darkblue", "#6ec6ff")
        ).grid(row=0, column=1, padx=5)

        self.lives_label = ctk.CTkLabel(
            bar, text=f"Tries left: {self.game.tries}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("darkred", "#ff6b6b")
        )
        self.lives_label.grid(row=0, column=2, padx=5)

        self.score_label = ctk.CTkLabel(
            bar, text=f"Score: {self.game.score}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("green", "#7fff7f")
        )
        self.score_label.grid(row=0, column=3, padx=5)

        ThemeToggleButton(
            self,
            current_theme=self.current_theme,
            on_toggle=self.on_toggle_theme
        ).place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=20)

        self.hangman_image_label = ctk.CTkLabel(main, text="")
        self.hangman_image_label.pack(pady=10)

        self.word_display = ctk.CTkLabel(
            main,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("darkblue", "#6ec6ff")
        )
        self.word_display.pack(pady=20)

        self._button_frame = ctk.CTkFrame(main, fg_color="transparent")
        self._button_frame.pack(expand=True, fill="both", pady=20)

    def _build_letter_buttons(self):
        self.buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            row, col = i // 13, i % 13
            btn = ctk.CTkButton(
                self._button_frame,
                text=letter,
                font=ctk.CTkFont(size=12),
                width=40, height=40,
                command=lambda l=letter: self.make_guess(l)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            self.buttons[letter] = btn
            self._button_frame.grid_columnconfigure(col, weight=1)

    def make_guess(self, letter):
        if self.buttons[letter].cget("state") == "disabled":
            return

        self.buttons[letter].configure(state="disabled", fg_color="gray")
        result = self.game.guess(letter)
        self.update_display()
        self.time_left = 15

        if result == "win":
            self._end_game("🎉 You won!")
        elif result == "lose":
            self._end_game(f"💀 You lose! The word was: {self.game.hidden_word}")

    def _handle_keypress(self, event):
        if self.game.game_over:
            return
        key = event.char.upper()
        if key.isalpha() and len(key) == 1 and key in self.buttons:
            self.make_guess(key)

    def start_timer(self):
        self.time_left = 15
        self._tick()

    def _tick(self):
        self.timer_label.configure(text=f"Time left: {self.time_left}s")

        if self.time_left > 0 and not self.game.game_over:
            self.time_left -= 1
            self.master.after(1000, self._tick)
        elif not self.game.game_over:
            result = self.game.timeout()
            self.update_display()
            if result == "lose":
                self._end_game("⏰ Time's up! No tries left!")
            else:
                self.time_left = 15
                self._tick()

    def update_display(self):
        self.word_display.configure(text=" ".join(self.game.guess_word))
        self.score_label.configure(text=f"Score: {self.game.score}")
        self.lives_label.configure(text=f"Tries left: {self.game.tries}")

        img = self.images[self.game.tries]
        if img:
            self.hangman_image_label.configure(image=img, text="")
        else:
            self.hangman_image_label.configure(image=None, text=f"Hangman {self.game.tries}",
                                               font=ctk.CTkFont(size=16))

    def _end_game(self, msg):
        self.game.game_over = True
        self.master.unbind("<Key>")
        for btn in self.buttons.values():
            btn.configure(state="disabled")

        GameDialog.show_result(self, msg, self.on_new_game)
