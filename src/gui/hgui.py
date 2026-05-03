import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

from src.logic.hlogic import HangmanLogic

# Set modern appearance
ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")  # "green", "dark-blue", etc.

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        
        # Use CTk's built-in fonts instead of global options
        ctk.CTkLabel  # Will inherit default styling
        
        # Bind key events
        self.master.bind("<Key>", self.handle_keypress)
        
        self.create_level_selection()

    def create_level_selection(self):
        # Clean up any existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(
            self.master,
            text="Hangman",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=40)

        level_label = ctk.CTkLabel(
            self.master,
            text="Select Level:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        level_label.pack(pady=10)

        self.level_var = ctk.StringVar(value="basic")
        self.level_var.trace_add("write", self.level_selected)

        level_menu = ctk.CTkOptionMenu(
            self.master,
            variable=self.level_var,
            values=["basic", "intermediate"],
            font=ctk.CTkFont(size=14)
        )
        level_menu.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self.master,
            text="Start Game",
            command=self.start_game,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.start_button.pack(pady=20)

        note_label = ctk.CTkLabel(
            self.master,
            text="Note: You can use the Keyboard!",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        note_label.pack(pady=10)

    def level_selected(self, *args):
        pass  # Handle level changes if needed

    def start_game(self):
        self.level = self.level_var.get()
        
        # Initialize game logic here
        self.game = HangmanLogic(level=self.level)  # Assuming this exists

        # Clear screen and build game UI
        for widget in self.master.winfo_children():
            widget.destroy()

        # Load images (add error handling)
        self.image_path = [f"images/hangman{i}.png" for i in range(6, -1, -1)]
        try:
            self.images = [ctk.CTkImage(
                light_image=Image.open(p).resize((200, 200)),
                size=(200, 200)
            ) for p in self.image_path]
        except Exception:
            self.images = [None] * 7  # Fallback

        self.create_widgets()
        self.update_display()
        self.start_timer()

    def create_widgets(self):
        # Status frame with grid layout
        status_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.timer_label = ctk.CTkLabel(
            status_frame,
            text="Time left: 15s",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="red"
        )
        self.timer_label.grid(row=0, column=0, padx=5)

        self.level_label_game = ctk.CTkLabel(
            status_frame,
            text=f"Level: {self.level.capitalize()}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="darkblue"
        )
        self.level_label_game.grid(row=0, column=1, padx=5)

        self.lives = ctk.CTkLabel(
            status_frame,
            text=f"Tries left: {self.game.tries}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="darkred"
        )
        self.lives.grid(row=0, column=2, padx=5)

        self.score_status = ctk.CTkLabel(
            status_frame,
            text=f"Score: {self.game.score}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="green"
        )
        self.score_status.grid(row=0, column=3, padx=5)

        # Center content frame
        main_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20)

        # Hangman image
        self.hangman_image_label = ctk.CTkLabel(main_frame, text="")
        self.hangman_image_label.pack(pady=10)

        # Word display
        self.word_display = ctk.CTkLabel(
            main_frame,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="darkblue"
        )
        self.word_display.pack(pady=20)

        # Button grid frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(expand=True, fill="both", pady=20)

        # Create alphabet buttons in grid (2 rows of 13)
        self.buttons = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            row = i // 13
            col = i % 13
            
            btn = ctk.CTkButton(
                button_frame,
                text=letter,
                font=ctk.CTkFont(size=12),
                width=40,
                height=40,
                command=lambda l=letter: self.make_guess(l)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            
            self.buttons[letter] = btn
            button_frame.grid_columnconfigure(col, weight=1)

    def make_guess(self, letter):
        if self.buttons[letter].cget("state") == "disabled":
            return  # Already guessed
            
        result = self.process_guess(letter)
        if result == "win":
            self.check_game_over("You won!")
        elif result == "lose":
            self.check_game_over(f"You lose! Correct word: {self.game.hidden_word}")

    def handle_keypress(self, event):
        if not hasattr(self, "game") or self.game.game_over:
            return

        key = event.char.upper()
        if key.isalpha() and len(key) == 1 and key in self.buttons:
            self.make_guess(key)

    def process_guess(self, letter):
        # Disable button visually
        self.buttons[letter].configure(state="disabled", fg_color="gray")
        
        result = self.game.guess(letter)
        self.update_display()
        self.time_left = 15  # Reset timer after guess
        return result

    def start_timer(self):
        self.time_left = 15
        self.update_timer()

    def update_timer(self):
        self.timer_label.configure(text=f"Time left: {self.time_left}s")

        if self.time_left > 0 and not self.game.game_over:
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        elif not self.game.game_over:
            self.game.tries -= 1
            self.lives.configure(text=f"Tries left: {self.game.tries}")
            self.update_display()
            if self.game.tries == 0:
                self.check_game_over("Time's up! No tries left!")
            else:
                self.time_left = 15
                self.update_timer()

    def update_display(self):
        self.word_display.configure(text=" ".join(self.game.guess_word))
        self.score_status.configure(text=f"Score: {self.game.score}")
        self.lives.configure(text=f"Tries left: {self.game.tries}")
        
        # Update hangman image
        if self.images[self.game.tries]:
            self.hangman_image_label.configure(image=self.images[self.game.tries])
        else:
            self.hangman_image_label.configure(text=f"Hangman {self.game.tries}", 
                                            font=ctk.CTkFont(size=16))

    def check_game_over(self, msg):
        self.game.game_over = True
        for btn in self.buttons.values():
            btn.configure(state="disabled")

        messagebox.showinfo("Game Over", msg)

        # New game button
        self.new_game_btn = ctk.CTkButton(
            self.master,
            text="New Game",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.new_game
        )
        self.new_game_btn.pack(pady=20)

    def new_game(self):
        self.create_level_selection()

# Usage:
if __name__ == "__main__":
    root = ctk.CTk()
    app = HangmanGUI(root)
    root.mainloop()