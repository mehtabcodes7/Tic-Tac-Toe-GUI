#Mehtab Codes Presents
#Tic Tac Toe Game Using Python
import tkinter as tk
from tkinter import messagebox
import random

# Main Tic Tac Toe class
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.theme = "light"  # Start with the light theme
        self.light_theme_colors = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "button_bg": "#ffffff",
            "button_fg": "#000000",
            "grid_bg": "#e6e6e6",
        }
        self.dark_theme_colors = {
            "bg": "#2c2c2c",
            "fg": "#ffffff",
            "button_bg": "#444444",
            "button_fg": "#ffffff",
            "grid_bg": "#333333",
        }
        self.current_colors = self.light_theme_colors
        self.mode = None  # Track game mode (single or multiplayer)

        self.main_menu()

    # Main menu setup
    def main_menu(self):
        self.apply_theme()

        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 24), bg=self.current_colors["bg"], fg=self.current_colors["fg"])
        label.pack(pady=20)

        play_button = tk.Button(self.root, text="Play", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.choose_mode)
        play_button.pack(pady=20)

        theme_button = tk.Button(self.root, text="Toggle Theme", font=("Helvetica", 14), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.toggle_theme)
        theme_button.pack(pady=10)

    # Apply the selected theme colors
    def apply_theme(self):
        colors = self.current_colors
        self.root.configure(bg=colors["bg"])

    # Toggle between light and dark themes
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.current_colors = self.dark_theme_colors
        else:
            self.theme = "light"
            self.current_colors = self.light_theme_colors
        self.main_menu()

    # Mode selection screen
    def choose_mode(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Choose Mode", font=("Helvetica", 24), bg=self.current_colors["bg"], fg=self.current_colors["fg"])
        label.pack(pady=20)

        single_player_button = tk.Button(self.root, text="Single Player", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.single_player)
        single_player_button.pack(pady=10)

        multiplayer_button = tk.Button(self.root, text="Multiplayer", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.multiplayer)
        multiplayer_button.pack(pady=10)

    # Single player mode setup
    def single_player(self):
        self.mode = "single"
        self.start_game()

    # Multiplayer mode setup
    def multiplayer(self):
        self.mode = "multi"
        self.start_game()

    # Start game
    def start_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False

        for widget in self.root.winfo_children():
            widget.destroy()

        self.grid_frame = tk.Frame(self.root, bg=self.current_colors["grid_bg"])
        self.grid_frame.pack(pady=20)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.grid_frame, text="", font=("Helvetica", 36), height=2, width=5, 
                               bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"],
                               command=lambda i=i: self.click(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        reset_button = tk.Button(self.root, text="Reset", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.start_game)
        reset_button.pack(side="left", padx=20)

        main_menu_button = tk.Button(self.root, text="Main Menu", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.main_menu)
        main_menu_button.pack(side="right", padx=20)

    # Click event for game
    def click(self, index):
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                self.end_game(f"{self.current_player} wins!")
            elif "" not in self.board:
                self.end_game("It's a tie!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O" and self.mode == "single":
                    self.ai_move()

    # AI move using minimax algorithm
    def ai_move(self):
        best_score = -float('inf')
        best_move = None

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        self.click(best_move)

    # Minimax algorithm for AI decision making
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"):
            return 1
        elif self.check_winner("X"):
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    # Check if the current player has won
    def check_winner(self, player):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(self.board[a] == self.board[b] == self.board[c] == player for a, b, c in win_conditions)

    # End game and display winner
    def end_game(self, result):
        self.game_over = True
        messagebox.showinfo("Game Over", result)

        # After the game, show "Play Again" and "Return to Main Menu" buttons
        for widget in self.root.winfo_children():
            widget.destroy()

        play_again_button = tk.Button(self.root, text="Play Again", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.start_game)
        play_again_button.pack(pady=10)

        main_menu_button = tk.Button(self.root, text="Return to Main Menu", font=("Helvetica", 18), bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"], command=self.main_menu)
        main_menu_button.pack(pady=10)

# Running the game
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x450")  # Adjust window size to be centered
    game = TicTacToe(root)
    root.mainloop()
