import customtkinter as ctk

class GameDialog:
    @staticmethod
    def show_result(parent, msg: str, on_new_game):
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Game Over")
        dialog.geometry("300x180")
        dialog.resizable(False, False)
        dialog.grab_set()  
        dialog.focus()
        dialog.protocol("WM_DELETE_WINDOW", lambda: GameDialog._on_close(dialog, on_new_game))

        ctk.CTkLabel(
            dialog,
            text=msg,
            font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=260
        ).pack(pady=30, padx=20)

        ctk.CTkButton(
            dialog,
            text="New Game",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838",
            command=lambda: GameDialog._on_close(dialog, on_new_game)
        ).pack(pady=10)

    @staticmethod
    def _on_close(dialog, on_new_game):
        dialog.destroy()
        on_new_game()