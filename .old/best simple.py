import tkinter as tk
from tkinter import ttk, messagebox
import random
from functools import partial

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("  Tic-Tac-Toe")
        self.master.geometry("500x500")
        self.master.configure(bg="#1e1e1e")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", foreground="#00ffff", background="#2a2a2a", font=("Arial", 16, "bold"))
        self.style.map("TButton", background=[("active", "#3a3a3a")])

        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.game_mode = tk.StringVar(value="single")
        self.difficulty = tk.StringVar(value="easy")
        self.player_score = {"X": 0, "O": 0}

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.master, text="  Tic-Tac-Toe", font=("Arial", 24, "bold"), fg="#00ffff", bg="#1e1e1e")
        title_label.pack(pady=20)

        # Game mode selection
        mode_frame = ttk.Frame(self.master)
        mode_frame.pack(pady=10)
        ttk.Radiobutton(mode_frame, text="Single Player", variable=self.game_mode, value="single").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Two Players", variable=self.game_mode, value="two").pack(side=tk.LEFT, padx=5)

        # Difficulty selection (for single player mode)
        diff_frame = ttk.Frame(self.master)
        diff_frame.pack(pady=10)
        ttk.Radiobutton(diff_frame, text="Easy", variable=self.difficulty, value="easy").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(diff_frame, text="Hard", variable=self.difficulty, value="hard").pack(side=tk.LEFT, padx=5)

        # Game board
        self.board_frame = ttk.Frame(self.master)
        self.board_frame.pack(pady=20)
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = ttk.Button(self.board_frame, text="", width=5,
                                    command=partial(self.make_move, i, j))
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

        # Score display
        self.score_label = tk.Label(self.master, text="X: 0 | O: 0", font=("Arial", 16), fg="#00ffff", bg="#1e1e1e")
        self.score_label.pack(pady=10)

        # Reset button
        reset_button = ttk.Button(self.master, text="New Game", command=self.reset_game)
        reset_button.pack(pady=10)

    def make_move(self, i, j):
        if self.board[i][j] == " ":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            
            if self.check_winner(self.current_player):
                self.end_game(f"{self.current_player} wins!")
                self.player_score[self.current_player] += 1
                self.update_score()
            elif self.is_board_full():
                self.end_game("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.game_mode.get() == "single" and self.current_player == "O":
                    self.make_ai_move()

    def make_ai_move(self):
        if self.difficulty.get() == "easy":
            self.make_random_move()
        else:
            self.make_best_move()

    def make_random_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.make_move(i, j)

    def make_best_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.make_move(*best_move)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def end_game(self, message):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        messagebox.showinfo("Game Over", message)

    def update_score(self):
        self.score_label.config(text=f"X: {self.player_score['X']} | O: {self.player_score['O']}")

    def reset_game(self):
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()